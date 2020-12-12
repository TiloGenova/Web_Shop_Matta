from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
# https://mdbootstrap.com/freebies/jquery/e-commerce/

def item_list(request):
    productsall = Product.objects.all()
    return render(request, 'main/home-page.html', {'products': productsall})


def home(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']


    productsall = Product.objects.all()
    productswomen = Product.objects.filter(gender='WOMAN')
    context = {'products': productsall, 'productswomen': productswomen, 'cartItems': cartItems}
    return render(request, 'main/home.html', context)


def base(request):
    return render(request, 'base.html', {})


def details(request, product_id):
    #ERRORHANDLING!?
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'main/details.html', {'product': product})



def cart(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'main/cart.html', context)




def checkout(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


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


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer, order = guestOrder(request, data)


    # Following block for logged in and not logged in users
    total = float(data['form']['total'])
    order.transaction_id = transaction_id


    if total == order.get_cart_total:
        order.complete = True
    order.save()


    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
        )




    return JsonResponse('Payment complete!', safe=False)
