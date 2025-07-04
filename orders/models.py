from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    OCCASION_CHOICES = [
        ('Birthday', 'Birthday'),
        ('Wedding', 'Wedding'),
        ('Anniversary', 'Anniversary'),
        ('Graduation', 'Graduation'),
        ('Other', 'Other'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cake_size_kg = models.DecimalField(max_digits=4, decimal_places=1)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    preferred_colors = models.CharField(max_length=100)
    toppings = models.CharField(max_length=200, blank=True, null=True)
    delivery_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"
