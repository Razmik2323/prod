from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Product, Order
from django.views.generic import (ListView, DetailView, 
                                  CreateView, UpdateView, 
                                  DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )

from .serializers import ProductSerializer, OrderSerializer


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


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'add_product'
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


class OrderExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest):
        orders = Order.objects.order_by('pk').all()
        response = {'orders': [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        }

        return JsonResponse(response)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]

    ordering_fields = [
        "pk",
        "name",
        "price",
    ]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = [
        "user",
        "delivery_address"

    ]
    ordering_fields = [
        "pk",
        "created_at",
    ]

    
