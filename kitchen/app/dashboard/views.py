from menu_orders.models import MenuOrder
from django.shortcuts import render


def home(request):
    """
    Dashboard for monitoring activity
    """
    orders = MenuOrder.objects.all().order_by('-created_at')

    return render(request, "home.html",
    {
        "orders": orders
    })