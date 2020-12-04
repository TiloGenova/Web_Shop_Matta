from django.contrib import admin
from .models import Product

# Register your models here.

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('category',)


admin.site.register(Product)

