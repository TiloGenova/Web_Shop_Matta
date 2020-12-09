from django.contrib import admin
from .models import Product, OrderItem, Order, Customer, ShippingAddress

# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('category',)


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

