from django.contrib import admin
from .models import Product, OrderItem, Order, Customer, ShippingAddress


# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('category',)



class OrderAdmin(admin.ModelAdmin):
    fields = [
        'customer',
        'date_ordered',
        'complete',
        'transaction_id',
    ]
    readonly_fields = ['date_ordered']
    class Meta:
        model = Order


class ProductAdmin(admin.ModelAdmin):
    fields = [
        'active',
        'date',
        'NEW_Flag',
        'gender',
        'size',
        'category',
        'title',
        'description',
        'text',
        'price',
        'discount_price',
        'discount_Flag',
        'image',
        'digital',
        'url',
    ]
    readonly_fields = ['date']
    class Meta:
        model = Product


class OrderItemAdmin(admin.ModelAdmin):
    fields = [
        'product',
        'order',
        'quantity',
        'date_added',
    ]
    readonly_fields = ['date_added']
    class Meta:
        model = OrderItem


class ShippingAddressAdmin(admin.ModelAdmin):
    fields = [
        'customer',
        'order',
        'address',
        'city',
        'state',
        'zipcode',
        'country',
        'date_added',

    ]
    readonly_fields = ['date_added']
    class Meta:
        model = ShippingAddress





admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
