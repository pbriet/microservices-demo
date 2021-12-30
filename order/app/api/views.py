from api.models import Order
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
# from saga.new_order import OrderSaga
from saga.models import OrderSagaTracker
from saga.new_order import OrderSagaManager

@csrf_exempt
def new_order(request):
    """
    API Call : new order from a customer

    (Called by either website/mobile app/whatever)
    """
    # Creating order in Database
    order = Order.objects.create(
        status='PENDING',
        menu=request.POST['menu'],
        payment_card_number=request.POST['payment_card_number'],
        payment_cvc=request.POST['payment_cvc']
    )

    tracker = OrderSagaTracker.objects.create(order=order, identifier=order.identifier)
    OrderSagaManager.start(tracker)

    return JsonResponse(order.serialize())


def dashboard(request):

    if request.method == 'POST':
        requests.post('http://localhost:9000/new-order',
            data={
                'payment_card_number': request.POST['payment_card_number'],
                'payment_cvc': request.POST['payment_cvc'],
                'menu': request.POST['menu']
            }
        )

    return render(request, "dashboard.html")