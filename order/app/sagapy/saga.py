from .rabbitmq import MessagingTransaction
import pika
import json


class SagaManager(object):
    """
    Creates a SagaManager object, that handles
    a Saga model.
    """

    STEPS = None
    SAGA_MODEL = None
    EXCHANGE_NAME = None

    @classmethod
    def start(cls, obj):
        """
        Starts the Saga
        """
        first_step = cls.STEPS[0]
        cls.send_message(first_step, obj)

    @classmethod
    def initialize_queues(cls):
        """
        Ensure that all necessary queues exist in RabbitMQ
        """
        with MessagingTransaction() as transaction:
            channel = transaction.channel
            channel.exchange_declare(cls.EXCHANGE_NAME, "direct",
                durable=True)
            for step in cls.STEPS:
                channel.queue_declare(queue=step.SEND_QUEUE)
                channel.queue_bind(step.SEND_QUEUE, cls.EXCHANGE_NAME, routing_key=step.SEND_QUEUE)
                if step.REPLY_QUEUE:
                    print("BIND reply queue", step.REPLY_QUEUE)
                    channel.queue_declare(queue=step.REPLY_QUEUE)
                    channel.queue_bind(step.REPLY_QUEUE, cls.EXCHANGE_NAME, routing_key=step.REPLY_QUEUE)

    @classmethod
    def get_next_step(cls, step):
        step_i = cls.STEPS.index(step)
        if step_i == len(cls.STEPS) - 1:
            # Last step
            return None
        return cls.STEPS[step_i + 1]

    @classmethod
    def get_previous_step(cls, step):
        step_i = cls.STEPS.index(step)
        if step_i == 0:
            # First step
            return None
        return cls.STEPS[step_i - 1]

    @classmethod
    def send_message(cls, step, obj, previous_step_data=None):
        """
        Execute given step by sending a message to microservice
        """
        if obj.status not in step.ALLOWED_STATES:
            raise Exception("Invalid state when proceeding saga step %s : %s (expected : %s)" % (
            step, obj.status, step.ALLOWED_STATES
        ))

        with MessagingTransaction() as transaction:
            message = step.get_message(obj, previous_step_data)

            transaction.channel.basic_publish(
                exchange=cls.EXCHANGE_NAME,
                routing_key=step.SEND_QUEUE,
                properties=pika.BasicProperties(
                    correlation_id=str(obj.identifier),
                    reply_to=step.REPLY_QUEUE
                ),
                body=json.dumps(message)
            )

    @classmethod
    def send_compensate(cls, step, obj):
        """
        Compensate given step by sending a message to microservice
        """
        with MessagingTransaction() as transaction:
            message = step.get_compensate_message(obj)

            transaction.channel.basic_publish(
                exchange=cls.EXCHANGE_NAME,
                routing_key=step.SEND_QUEUE,
                properties=pika.BasicProperties(
                    correlation_id=str(obj.identifier)
                ),
                body=json.dumps(message)
            )

    @classmethod
    def consume_reply_queues(cls):
        """
        Starts a listener process, watching for replies in
        queues.
        """
        with MessagingTransaction() as transaction:
            for step in cls.STEPS:

                def on_reply(ch, method, props, body, st=step):
                    try:
                        # Retrieve the Saga object from the identifier
                        obj = cls.SAGA_MODEL.objects.get(identifier=props.correlation_id)

                        # Custom Protocol : should be JSON structured this way
                        # { 'status': 'ok', 'data': { ... } }
                        # { 'status': 'fail': 'data': { ... }}
                        # { 'status': 'compensate': 'data': { ... }}
                        data = json.loads(body)

                        if data['status'] == 'ok':
                            # Success call. Save state.
                            st.update_object_on_success(obj, data)
                            # Send next message in SAGA
                            next_step = cls.get_next_step(st)
                            if next_step is not None:
                                cls.send_message(next_step, obj, data)
                        elif data['status'] == 'fail':
                            # Failed operation. Save state
                            st.update_object_on_failure(obj, data)
                        elif data['status'] == 'compensate':
                            # Compensated operation. Save state
                            st.update_object_on_compensate(obj, data)
                        else:
                            raise Exception("unknown status : %s" % body['status'])

                        if data['status'] in ('fail', 'compensate'):
                            # Compensation/failure
                            # Call compensation on previous step
                            cls.send_compensate(cls.get_previous_step(st), obj)
                    finally:
                        ch.basic_ack(delivery_tag = method.delivery_tag)

                transaction.channel.basic_consume(
                    queue=step.REPLY_QUEUE,
                    on_message_callback=on_reply)

            print(' [*] Waiting for messages')
            transaction.channel.start_consuming()

