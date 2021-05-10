from django import forms

from orders.models import Orders


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['customer_name', 'phone_number', 'email']
