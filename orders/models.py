from io import BytesIO

import qrcode
from PIL import Image, ImageDraw
from django.core.files import File
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from products.models import Product


class Orders(models.Model):
    order_number = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    email = models.EmailField(max_length=254)
    confirm = models.BooleanField(default=False)
    grand_total_price = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, default='')

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if self.confirm is True:
            input_data = 'Name: ' + self.customer_name + '\nPhone: ' + self.phone_number + '\nEmail: ' + self.email
            print(input_data)
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
            qr.add_data(input_data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            fname = f'qr_code-{self.customer_name}.png'
            buffer = BytesIO()
            img.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)


class AddItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
