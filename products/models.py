from django.db import models

# Create your models here.


class Product(models.Model):
    product_code = models.CharField(max_length=10, unique=True)
    product_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


