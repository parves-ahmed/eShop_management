from django.db import models

# Create your models here.


class Product(models.Model):
    product_code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(decimal_places=2, max_digits=4)
    quantity = models.DecimalField(decimal_places=2, max_digits=4)


