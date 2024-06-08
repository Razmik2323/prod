from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect

from .forms import ProductForm, OrderForm
from .models import Product, Order


def shop_index(request: HttpRequest):
    return render(request, 'shopapp/shop-index.html')

def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related('products').all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)

def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:products_list')
            return redirect(url)
    else:
        form = ProductForm()

    context = {
        'form': form
    }

    return render(request, 'shopapp/create-product.html', context=context)


def create_orders(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:orders_list')
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        'form': form
    }

    return render(request, 'shopapp/create-order.html', context=context)



