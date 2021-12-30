from sagapy.step import SagaStep

class DeliveryStep(SagaStep):

    SEND_QUEUE = "incoming_delivery"
    REPLY_QUEUE ="processed_delivery"

    ALLOWED_STATES = ('PAYMENT_OK',)

    def get_message(self, saga_obj, previous_step_data=None):
        """
        Returns the message sent to the microservice
        """
        return {
            'cooked_at': previous_step_data['estimated_cooked_time']
        }

    def update_object_on_success(self, saga_obj, data):
        """
        Update the Saga object from data returned by success call to
        the microservice
        """
        print("Delivery schedul success !", data)
        saga_obj.status = 'KITCHEN_SCHEDULED'
        saga_obj.save()

    def update_object_on_compensate(self, saga_obj, data):
        """
        Update the Saga object from data returned when the microservices
        compensated
        """
        saga_obj.status = 'KITCHEN_CANCELLED'
        saga_obj.save()

    def update_object_on_failure(self, saga_obj, data):
        """
        Update the Saga object from data returned by failed call to
        the microservice
        """
        saga_obj.status = 'KITCHEN_FAILED'
        saga_obj.save()