import decimal
from decimal import Decimal

import json
from io import BytesIO

import qrcode
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import get_template
from django.urls import reverse
from num2words import num2words
from xhtml2pdf import pisa

from products.models import Product
from .forms import OrderForm
from .models import Orders, AddItem


def order_list(request):
    orders = Orders.objects.all()
    return render(request, 'order/order_list.html', {'orders': orders})


def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            order.save()
            print(order.id)
            return HttpResponseRedirect(reverse('order_product', args=[order.id]))
        return render(request, 'order/add_order.html', {'order_form': order_form})
    else:
        order_form = OrderForm()
        return render(request, 'order/add_order.html', {'order_form': order_form})


def order_product(request, order_id):
    print(order_id)
    order = Orders.objects.get(pk=order_id)
    total_item = AddItem.objects.filter(order_id=order.id).count()
    products = Product.objects.filter(quantity__gt=0)
    if request.method == 'GET':
        product_id = request.GET.get('product_id', None)
        product_code = request.GET.get('product_code', None)
        if product_id is not None and product_id != '':
            products = Product.objects.filter(pk=product_id)
            return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
        if product_code is not None and product_code != '':
            products = Product.objects.filter(product_code=product_code)
            return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
    return render(request, 'order/order_product.html', {'products': products, 'order': order, 'total_item': total_item})


def order_details(request, order_id):
    print(order_id)
    order = get_object_or_404(Orders, pk=order_id)
    items = AddItem.objects.filter(order_id=order.id)
    return render(request, 'order/order_details.html', {'order': order, 'items': items})


def confirm_order(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if request.method == 'POST':
        data = json.loads(request.POST.get('arrData', None))
        if order.confirm is False:
            grand_total = decimal.Decimal(0)
            for d in data:
                item = AddItem.objects.get(pk=d['item_id'], order_id=d['order_id'])
                product = Product.objects.get(pk=item.product_id)
                product.quantity = product.quantity - int(d['quantity'])
                grand_total += decimal.Decimal(d['total_price'])
                print(product.quantity)
                product.save()
            order.confirm = True
            order.grand_total_price = grand_total
            print(order.confirm, order.grand_total_price)
            order.save()
            return JsonResponse({'msg': 'Saved'}, safe=False)
        else:
            return JsonResponse({'msg': 'Exist'}, safe=False)
    return JsonResponse('ok', safe=False)


def order_invoice(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    items = AddItem.objects.filter(order_id=order.id)
    amount = num2words(order.grand_total_price).capitalize()
    return render(request, 'order/order_invoice.html', {'order': order, 'items': items, 'amount': amount})


def add_item(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        product_id = request.POST.get('product_id', None)
        quantity = request.POST.get('quantity', None)
        price = request.POST.get('total_price', None)
        order = get_object_or_404(Orders, pk=order_id)
        product = get_object_or_404(Product, pk=product_id)
        if order is not None and product is not None:
            if int(product.quantity) > 0:
                try:
                    item = AddItem.objects.get(order_id=order.id, product_id=product.id)
                    item.quantity += int(quantity)
                    item.total_price += decimal.Decimal(price)
                    print(item.quantity, item.total_price)
                    item.save()
                except AddItem.DoesNotExist:
                    AddItem.objects.create(order=order, product=product, quantity=quantity, total_price=price)
                    print('created')
                total_item = AddItem.objects.filter(order_id=order.id).count()
                return JsonResponse({'stock': product.quantity, 'total_item': total_item}, safe=False)
    return JsonResponse('ok', safe=False)


def update_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id', None)
        order_id = request.POST.get('order_id', None)
        quantity = request.POST.get('quantity', None)
        total_price = request.POST.get('total_price', None)
        item = AddItem.objects.get(pk=item_id, order_id=order_id)
        if item and quantity is not None and total_price is not None:
            item.quantity = quantity
            item.total_price = total_price
            item.save()
            return JsonResponse({'quantity': item.quantity, 'total_price': item.total_price}, safe=False)
    return JsonResponse('Something went wrong', safe=False)


def delete_item(request, item_id):
    item = get_object_or_404(AddItem, pk=item_id)
    if item is not None:
        order_id = item.order.pk
        item.delete()
        return HttpResponseRedirect(reverse('order_details', args=[order_id]))


def download_invoice(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    items = AddItem.objects.filter(order_id=order.id)
    amount = num2words(order.grand_total_price).capitalize()
    data = {'items': items, 'order': order, 'amount': amount}
    template = get_template('order/download_invoice.html')
    data_p = template.render(data)
    response = BytesIO()

    pdf_page = pisa.pisaDocument(BytesIO(data_p.encode('utf-8')), response)
    if not pdf_page.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error Generating Pdf')
