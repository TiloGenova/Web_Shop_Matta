from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
import json

# Create your views here.
# https://mdbootstrap.com/freebies/jquery/e-commerce/

def item_list(request):
    productsall = Product.objects.all()
    return render(request, 'main/home-page.html', {'products': productsall})


def home(request):


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        items = []   # if user is not logged in
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']



    productsall = Product.objects.all()
    productswomen = Product.objects.filter(gender='WOMAN')
    context = {'products': productsall, 'productswomen': productswomen, 'cartItems':cartItems}
    return render(request, 'main/home.html', context)


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
        cartItems = order.get_cart_items
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        items = []   # if user is not logged in
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'main/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        items = []   # if user is not logged in
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'main/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductID:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()


    return JsonResponse('Item was added YEAH', safe=False)  # to just to return a message   no template