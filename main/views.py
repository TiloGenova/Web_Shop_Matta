from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def home(request):

    productsall = Product.objects.all()
    productswomen = Product.objects.filter(gender='WOMAN')
    return render(request, 'home.html', {'products': productsall, 'productswomen': productswomen})


def base(request):
    return render(request, 'base.html', {'home': home})


def details(request, product_id):
    #ERRORHANDLING!?
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'details.html', {'product': product})



def cart(request):

    return render(request, 'cart.html', {})
