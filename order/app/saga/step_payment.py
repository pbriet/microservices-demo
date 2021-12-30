from sagapy.step import SagaStep

class PaymentStep(SagaStep):

    SEND_QUEUE = "incoming_payment"
    REPLY_QUEUE ="processed_payment"

    ALLOWED_STATES = ('CREATED',)

    def get_message(self, saga_obj, previous_step_data=None):
        """
        Returns the message sent to the microservice
        """
        order = saga_obj.order

        return {
            'payment_card_details': {
                'number': order.payment_card_number,
                'cvc': order.payment_cvc
            }
        }

    def update_object_on_success(self, saga_obj, data):
        """
        Update the Saga object from data returned by success call to
        the microservice
        """
        print("step payment successsss !")
        saga_obj.status = 'PAYMENT_OK'
        saga_obj.save()

    def update_object_on_compensate(self, saga_obj, data):
        """
        Update the Saga object from data returned when the microservices
        compensated
        """
        saga_obj.status = 'PAYMENT_CANCELLED'
        saga_obj.save()

    def update_object_on_failure(self, saga_obj, data):
        """
        Update the Saga object from data returned by failed call to
        the microservice
        """
        saga_obj.status = 'PAYMENT_FAILED'
        saga_obj.save()