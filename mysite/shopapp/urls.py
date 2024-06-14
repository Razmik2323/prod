from django.urls import path

from .views import (
    shop_index,
    create_product, 
    create_orders, 
    ProductsDetailsView,
    ProductsListView,
    OrdersListView,
    )

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductsDetailsView.as_view(), name='products_details'),
    path('products/create/', create_product, name='product_create'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create', create_orders, name='orders_create'),

]
