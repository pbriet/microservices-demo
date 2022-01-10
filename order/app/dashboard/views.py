from api.models import Order
from django.shortcuts import render
from saga.models import OrderSagaTracker


def home(request):
    """
    Dashboard for monitoring activity
    """
    orders = Order.objects.all().order_by('-created_at')
    trackers = OrderSagaTracker.objects.all().order_by('-created_at')

    return render(request, "home.html",
    {
        "orders": orders,
        "trackers": trackers
    })