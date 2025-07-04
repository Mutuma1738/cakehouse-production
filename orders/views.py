# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from products.models import Product
from django.contrib.auth.decorators import login_required
import sweetify
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.utils import timezone

@login_required
def create_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        cake_size = request.POST.get('cake_size_kg')
        occasion = request.POST.get('occasion')
        colors = request.POST.get('preferred_colors')
        toppings = request.POST.get('toppings')
        delivery_date_str = request.POST.get('delivery_date')

        # Convert string to datetime
        delivery_date_naive = datetime.strptime(delivery_date_str, '%Y-%m-%dT%H:%M')
        # Make it timezone aware
        delivery_date = timezone.make_aware(delivery_date_naive)

        order = Order.objects.create(
            product=product,
            customer=request.user,
            cake_size_kg=cake_size,
            occasion=occasion,
            preferred_colors=colors,
            toppings=toppings,
            delivery_date=delivery_date,  # Now it's timezone aware
            paid=False
        )

        # Send confirmation email after order is successfully created
        send_mail(
            'Order Confirmation',
            'Your order has been received and is being processed.',
            settings.DEFAULT_FROM_EMAIL,
            [order.customer.email],
            fail_silently=False,
        )

        sweetify.success(request, 'Order placed successfully! Proceed to payment.')
        return redirect('order_success')

    return render(request, 'orders/order_form.html', {'product': product})

def order_success(request):
    return render(request, 'orders/order_success.html')
