from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
# https://mdbootstrap.com/freebies/jquery/e-commerce/

def item_list(request):
    productsall = Product.objects.all()
    return render(request, 'main/home-page.html', {'products': productsall})


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




def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        items = []   # if user is not logged in
        order = {'get_cart_total':0, 'get_cart_items':0}


    context = {'items': items, 'order': order}
    return render(request, 'main/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        items = []   # if user is not logged in
        order = {'get_cart_total':0, 'get_cart_items':0}


    context = {'items': items, 'order': order}
    return render(request, 'main/checkout.html', context)
