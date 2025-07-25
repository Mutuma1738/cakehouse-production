from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_1kg = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
