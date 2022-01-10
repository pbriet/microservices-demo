import json
from api.models import Order

def handle_cooked_meal(ch, method, props, body):
    """
    New menu to prepare, incoming
    """
    print("ORDER : received kitchen/cooked event", props)
    data = json.loads(body)
    identifier = data['identifier']

    order = Order.objects.get(identifier=identifier)
    order.status = 'COOKED'
    order.save()