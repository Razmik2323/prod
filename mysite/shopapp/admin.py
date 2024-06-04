from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archived products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchived products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name', 'description_short'
    search_fields = 'name', 'price'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount')
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',)
        }),
    ]


    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'user_verbose', 'delivery_address', 'promocode', 'created_at'
    list_display_links = 'pk', 'user_verbose', 'delivery_address'
    search_fields = 'user_verbose', 'delivery_address', 'promocode'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')


    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username





