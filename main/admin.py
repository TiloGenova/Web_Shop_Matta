from django.contrib import admin
from .models import Product, OrderItem, Order, Customer, ShippingAddress, User, ShippingCost


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'customer',
        'date_ordered',
        'complete',
        'transaction_id',
    ]
    list_display =[
        'id',
        'customer',
        'date_ordered',
        'complete',
        'transaction_id',
    ]

    ordering = ('date_ordered', 'complete',)
    search_fields = ('customer', 'date_ordered')
    list_filter = ('transaction_id',)


    readonly_fields = ['date_ordered','id']

    class Meta:
        model = Order


def disactivate(modeladmin, request, queryset):
    queryset.update(active=False)
disactivate.short_description = 'Disactivate products'



def activate(modeladmin, request, queryset):
    queryset.update(active=True)
activate.short_description = 'Activate products'




class ProductAdmin(admin.ModelAdmin):
    actions = [disactivate, activate]
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
        'stock',
        'digital',
        'url',
    ]
    list_display =[

        'title',
        'stock',
        'id',
        'size',
        'gender',
        'active',
        'date',
        'NEW_Flag',
        'category',
        'price',
        'discount_price',
        'discount_Flag',
        'image',
        'digital',
        'url',
    ]

    readonly_fields = ['date', 'id']



    class Meta:
        model = Product







class OrderItemAdmin(admin.ModelAdmin):
    fields = [
        'product',
        'order',
        'quantity',
        'date_added',
    ]

    list_display =[
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

    list_display =['customer',
                   'order',
                   'address',
                   'city',
                   'state',
                   'zipcode',
                   'country',
                   'date_added',]

    readonly_fields = ['date_added']
    class Meta:
        model = ShippingAddress



class CustomerAdmin(admin.ModelAdmin):
    fields = [

        'user',
        'name',
        'email',

    ]
    list_display =[
        'id',
        'user',
        'name',
        'email',
    ]

    readonly_fields = ['id',]

    class Meta:
        model = Customer


class UserAdmin(admin.ModelAdmin):
    fields = [


    ]
    list_display =[
        'id',

    ]

    readonly_fields = ['id',]

    class Meta:
        model = User


class ShippingCostAdmin(admin.ModelAdmin):
    fields = [
        'costs',
        'service',


    ]
    list_display =[
        'id',
        'costs',
        'service',

    ]

    readonly_fields = ['id',]

    class Meta:
        model = ShippingCost





admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ShippingCost, ShippingCostAdmin)
