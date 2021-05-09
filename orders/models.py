from django.db import models

# Create your models here.
from products.models import Product


class Orders(models.Model):
    order_number = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=254)
    confirm = models.BooleanField(default=False)
    grand_total_price = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class AddItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(decimal_places=2, max_digits=4, default=0)
