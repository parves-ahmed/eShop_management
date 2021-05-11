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
    # Get all order & show them in order_list
    orders = Orders.objects.all()
    return render(request, 'order/order_list.html', {'orders': orders})


def add_order(request):
    if request.method == 'POST':
        # Get the form with values
        # Mainly customer info get inputs here
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # If valid then save
            order = order_form.save()
            order.save()
            return HttpResponseRedirect(reverse('order_product', args=[order.id]))
        # if form is not valid, reload page with form, values and errors
        return render(request, 'order/add_order.html', {'order_form': order_form})
    else:
        # Mainly in initial stage, the page load with empty form
        order_form = OrderForm()
        return render(request, 'order/add_order.html', {'order_form': order_form})


# This function load product that will be added
# to order & return search result
def order_product(request, order_id):
    order = Orders.objects.get(pk=order_id)
    if order.confirm is False:
        # Count total item added to order
        total_item = AddItem.objects.filter(order_id=order.id).count()
        # Find the product which quantity > 0
        # otherwise it will not show
        products = Product.objects.filter(quantity__gt=0)
        if request.method == 'GET':
            # Get product_id & product_code
            product_id = request.GET.get('product_id', None)
            product_code = request.GET.get('product_code', None)
            # Search through product_id
            if product_id is not None and product_id != '':
                products = Product.objects.filter(pk=product_id)
                return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
            # Search through product_code
            if product_code is not None and product_code != '':
                products = Product.objects.filter(product_code=product_code)
                return JsonResponse({'products': list(products.values()), 'order_id': order.id}, safe=False)
        return render(request, 'order/order_product.html', {'products': products, 'order': order, 'total_item': total_item})
    else:
        # If order.confirm is true redirect to order_invoice
        return HttpResponseRedirect(reverse('order_invoice', args=[order.id]))


# This function return all products which
# are added in order_product stage
def order_details(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if order.confirm is False:
        items = AddItem.objects.filter(order_id=order.id)
        return render(request, 'order/order_details.html', {'order': order, 'items': items})
    else:
        # If order.confirm is true redirect to order_invoice
        return HttpResponseRedirect(reverse('order_invoice', args=[order.id]))


# When all product addition is done, confirm it
def confirm_order(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    if request.method == 'POST':
        data = json.loads(request.POST.get('arrData', None))
        if order.confirm is False:
            # if order.confirm is false update product quantity &
            # set order.confirm = true, set order.grand_total
            grand_total = decimal.Decimal(0)
            for d in data:
                item = AddItem.objects.get(pk=d['item_id'], order_id=d['order_id'])
                product = Product.objects.get(pk=item.product_id)
                # update product quantity
                product.quantity = product.quantity - int(d['quantity'])
                # calculate grand_total
                grand_total += decimal.Decimal(d['total_price'])
                print(product.quantity)
                product.save()
            # set order.confirm & grand_total
            order.order_number = '{}{}'.format('order_', order.id)
            order.confirm = True
            order.grand_total_price = grand_total
            print(order.confirm, order.grand_total_price)
            # The QR code will generate on this stage while saving order,
            # because order.confirm will turn into true here
            order.save()
            return JsonResponse({'msg': 'Saved'}, safe=False)
        else:
            # order.confirm is not false, then it exists already
            return JsonResponse({'msg': 'Exist'}, safe=False)
    return JsonResponse('ok', safe=False)


# Generate invoice html file after confirm order
def order_invoice(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    items = AddItem.objects.filter(order_id=order.id)
    # convert currency to word
    amount = num2words(order.grand_total_price).capitalize()
    return render(request, 'order/order_invoice.html', {'order': order, 'items': items, 'amount': amount})


# Add item in order_product stage
def add_item(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        product_id = request.POST.get('product_id', None)
        quantity = request.POST.get('quantity', None)
        price = request.POST.get('total_price', None)
        # Find order & product
        order = get_object_or_404(Orders, pk=order_id)
        product = get_object_or_404(Product, pk=product_id)
        print(product.quantity)
        if order is not None and product is not None:
            try:
                item = AddItem.objects.get(order_id=order.id, product_id=product.id)
                # if item already exist & product quantity > item quantity,
                # then just update item quantity & item total price
                if product.quantity > item.quantity:
                    item.quantity += int(quantity)
                    item.total_price += decimal.Decimal(price)
                    print(item.quantity, item.total_price)
                    item.save()
                else:
                    return JsonResponse({'msg': 'Stock out'}, safe=False)
            except AddItem.DoesNotExist:
                # otherwise create new
                AddItem.objects.create(order=order, product=product, quantity=quantity, total_price=price)
                print('created')
            # Count total item added and return response
            total_item = AddItem.objects.filter(order_id=order.id).count()
            return JsonResponse({'stock': product.quantity, 'total_item': total_item}, safe=False)
    return JsonResponse('ok', safe=False)


def update_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id', None)
        order_id = request.POST.get('order_id', None)
        quantity = request.POST.get('quantity', None)
        total_price = request.POST.get('total_price', None)

        # Get item by item_id and order_id, if exist update it
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
    # Find the template and render it
    template = get_template('order/download_invoice.html')
    html = template.render(data)
    # Generate Django response object & set content_type pdf
    response = HttpResponse(content_type='application/pdf')
    # For download
    response['content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create pdf
    pdf_page = pisa.CreatePDF(html, dest=response)
    # if no error return response
    if not pdf_page.err:
        return response
    else:
        return HttpResponse('Error Generating Pdf')
