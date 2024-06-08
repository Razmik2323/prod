from django.urls import path

from .views import shop_index, products_list, orders_list, create_product, create_orders

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', products_list, name='products_list'),
    path('products/create/', create_product, name='product_create'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/create', create_orders, name='orders_create'),

]
