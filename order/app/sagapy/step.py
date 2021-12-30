
class SagaStep(object):
    """
    Saga STEP
    """
    SEND_QUEUE = None # RabbitMQ queue name
    REPLY_QUEUE = None  # RabbitMQ queue name (TODO : mono-saga reply queue ?)

    ALLOWED_STATES = tuple() # List of states allowed when executing step forward

    def get_message(self, saga_obj, previous_step_data=None):
        """
        Returns the message sent to the microservice
        """
        raise NotImplementedError

    def get_compensate_message(self, saga_obj):
        """
        Returns the message sent to the microservice to compensate
        in case of failure in following steps
        """

    def update_object_on_success(self, saga_obj, data):
        """
        Update the Saga object from data returned by success call to
        the microservice
        """
        raise NotImplementedError

    def update_object_on_compensate(self, saga_obj, data):
        """
        Update the Saga object from data returned when the microservices
        compensated
        """
        raise NotImplementedError

    def update_object_on_failure(self, saga_obj, data):
        """
        Update the Saga object from data returned by failed call to
        the microservice
        """
        raise NotImplementedError
