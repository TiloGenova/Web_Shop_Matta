from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def item_list(request):
    productsall = Product.objects.all()
    return render(request, 'main/item_list.html', {'products': productsall})


def home(request):

    productsall = Product.objects.all()
    productswomen = Product.objects.filter(gender='WOMAN')
    return render(request, 'main/home.html', {'products': productsall, 'productswomen': productswomen})


def base(request):
    return render(request, 'base.html', {})


def details(request, product_id):
    #ERRORHANDLING!?
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'main/details.html', {'product': product})


