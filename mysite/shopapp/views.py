from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect

from .forms import ProductForm, OrderForm
from .models import Product, Order
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def shop_index(request: HttpRequest):
    return render(request, 'shopapp/shop-index.html')



class ProductsDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'



class ProductsListView(ListView):
    template_name = 'shopapp/products-list.html'
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


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

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
    

class OrdersListView(ListView):
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))


class OrdersDetailsView(DetailView):
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))

class CreateOrderView(CreateView):
    model = Order
    fields = "user", "products", "dilivery_adress", "promocode"
    success_url = reverse_lazy("shopapp:orders_list")





