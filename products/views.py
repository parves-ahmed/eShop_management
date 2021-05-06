from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from .forms import ProductForm
from .models import Product


def index(request):
    context = 'hello'
    return render(request, 'base.html', {'context': context})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        print('ok')
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            product.save()
            msg = 'saved'
            print(product.product_name)
            return JsonResponse({'msg': msg, 'productName': product.product_name})
        return render(request, 'product/add_product.html', {'product_form': product_form})
    else:
        product_form = ProductForm()
        return render(request, 'product/add_product.html', {'product_form': product_form})


def product_update(request, id=None):
    product = get_object_or_404(Product, pk=id)
    print(product)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_save = product_form.save()
            print('update', product_save.product_name)
            return HttpResponseRedirect(reverse('product_list'))
        return render(request, 'product/product_update.html', {'product_form': product_form})
    else:
        product_form = ProductForm(instance=product)
        return render(request, 'product/product_update.html', {'product_form': product_form})


def product_delete(request, id=None):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'DELETE':
        product.delete()
        return HttpResponseRedirect(reverse('product_list'))
