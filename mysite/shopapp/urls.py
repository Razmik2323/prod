from django.urls import path

from .views import (
    shop_index, ProductsDetailsView,
    ProductsListView, OrdersListView,
    OrdersDetailsView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    CreateOrderView, OrderUpdateView,
    OrderDeleteView, OrderExportView,
)

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),

    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductsDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),

    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create/', CreateOrderView.as_view(), name='order_create'),
    path('orders/<int:pk>/', OrdersDetailsView.as_view(), name='order_delails'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/export/', OrderExportView.as_view(), name='orders-export'),


]
