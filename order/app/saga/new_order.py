
from sagapy.saga import SagaManager
from saga.step_payment import PaymentStep
from saga.step_kitchen import KitchenStep
from saga.step_delivery import DeliveryStep
from saga.models import OrderSagaTracker

class OrderSagaManager(SagaManager):

    STEPS = [
        PaymentStep(),
        KitchenStep(),
        DeliveryStep()
    ]

    SAGA_MODEL = OrderSagaTracker

    EXCHANGE_NAME = "order_saga"

