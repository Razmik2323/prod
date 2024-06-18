from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, reverse, redirect

from .forms import ProductForm, OrderForm
from .models import Product, Order
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy


def shop_index(request: HttpRequest):
    return render(request, 'shopapp/shop-index.html')



class ProductsDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'



class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    model = Product
    context_object_name = 'products'



class OrdersListView(ListView):
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))


class OrdersDetailsView(DetailView):
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))



class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return reverse('shopapp:products_details',
                       kwargs={'pk': self.object.pk},
                       )


def create_orders(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:order_list')
            return redirect(url)
    else:
        form = OrderForm()

    context = {
        'form': form
    }

    return render(request, 'shopapp/create-order.html', context=context)



