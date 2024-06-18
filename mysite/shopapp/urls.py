from django.urls import path

from .views import (
    shop_index,
    create_orders, 
    ProductsDetailsView,
    ProductsListView,
    OrdersListView,
    OrdersDetailsView,
    ProductCreateView,
    ProductUpdateView,
    )

app_name = 'shopapp'
urlpatterns = [
    path('', shop_index, name='index'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductsDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='products_update'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrdersDetailsView.as_view(), name='order_delails'),
    path('orders/create', create_orders, name='orders_create'),

]
