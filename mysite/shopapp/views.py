from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, reverse

from .models import Product, Order
from django.views.generic import (ListView, DetailView, 
                                  CreateView, UpdateView, 
                                  DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )

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


class ProductCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.has_perm("shopapp.add_product")
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if self.request.user.has_perm("shopapp.change_product") and self.get_object().created_by == self.request.user:
            return True
        else:
            return False

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


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))


class OrdersDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "view_order"
    queryset = (Order.objects.select_related('user')
                .prefetch_related('products'))


class CreateOrderView(CreateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('shopapp:orders_detail',
                       kwargs={'pk': self.object.pk},
                       )
    

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')
    
