from decimal import Decimal

import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from products.models import Product
from .forms import OrderForm
from .models import Orders, AddItem


def add_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            order.save()
            return HttpResponseRedirect(reverse('order_product', args=[order.id]))
        return render(request, 'order/add_order.html', {'order_form': order_form})
    else:
        order_form = OrderForm()
        return render(request, 'order/add_order.html', {'order_form': order_form})


def order_product(request, order_id):
    print(order_id)
    order = Orders.objects.get(pk=order_id)
    total_item = AddItem.objects.filter(order_id=order.id).count()
    product_id = request.GET.get('product_id', None)
    product_code = request.GET.get('product_code', None)
    if product_id is not None and product_id != '':
        products = Product.objects.filter(pk=product_id)
        return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
    elif product_code is not None and product_code != '':
        products = Product.objects.filter(product_code=product_code)
        return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
    else:
        products = Product.objects.filter(quantity__gt=0)
    return render(request, 'order/order_product.html', {'products': products, 'order': order, 'total_item': total_item})


def order_details(request, order_id):
    print(order_id)
    order = get_object_or_404(Orders, pk=order_id)
    items = AddItem.objects.filter(order_id=order.id)
    return render(request, 'order/order_details.html', {'order': order, 'items': items})


def confirm_order(request):
    data = json.loads(request.POST.get('arrData', None))
    for d in data:
        print(d['item_id'])
    # print(type(data))
    return JsonResponse('ok', safe=False)


def add_item(request):
    order_id = request.GET.get('order_id', None)
    product_id = request.GET.get('product_id', None)
    quantity = request.GET.get('quantity', None)
    total_price = request.GET.get('total_price', None)
    order = get_object_or_404(Orders, pk=order_id)
    product = get_object_or_404(Product, pk=product_id)
    if order is not None and product is not None:
        if int(product.quantity) > 0:
            AddItem.objects.create(order=order, product=product, quantity=quantity, total_price=total_price)
            total_item = AddItem.objects.filter(order_id=order.id).count()
            return JsonResponse({'stock': product.quantity, 'total_item': total_item}, safe=False)
    return JsonResponse('Not saved', safe=False)


def update_item(request):
    item_id = request.GET.get('item_id', None)
    order_id = request.GET.get('order_id', None)
    quantity = request.GET.get('quantity', None)
    total_price = request.GET.get('total_price', None)
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
