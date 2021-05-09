from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from .forms import ProductForm
from .models import Product


def index(request):
    context = 'hello'
    return HttpResponseRedirect(reverse('product_list'))


def product_list(request):
    # Get all products & show product_list
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        # Get the form
        product_form = ProductForm(request.POST)
        # If the form is valid then save and
        # Redirect to product_list page
        if product_form.is_valid():
            product = product_form.save()
            product.save()
            print(product.product_name)
            return HttpResponseRedirect(reverse('product_list'))
        return render(request, 'product/add_product.html', {'product_form': product_form})
    else:
        product_form = ProductForm()
        return render(request, 'product/add_product.html', {'product_form': product_form})


def product_update(request, id=None):
    # Get the product if exists or return 404
    product = get_object_or_404(Product, pk=id)
    print(product)
    if request.method == 'POST':
        # Get the form with product
        product_form = ProductForm(request.POST, instance=product)
        # If the form is valid then save and
        # Redirect to Product_list page
        if product_form.is_valid():
            product_save = product_form.save()
            print('update', product_save.product_name)
            return HttpResponseRedirect(reverse('product_list'))
        return render(request, 'product/product_update.html', {'product_form': product_form})
    else:
        product_form = ProductForm(instance=product)
        return render(request, 'product/product_update.html', {'product_form': product_form})


def product_delete(request, id=None):
    # Get the product if exists or return 404
    product = get_object_or_404(Product, pk=id)
    if request.method == 'DELETE':
        # Delete the product
        product.delete()
        return JsonResponse('Deleted', safe=False)
    return HttpResponseRedirect(reverse('product_list'))
