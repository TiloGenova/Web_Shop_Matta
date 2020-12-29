from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import cookieCart, cartData, guestOrder
import sqlite3
from decimal import Decimal


# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                email = form.cleaned_data.get('email')
                name = form.cleaned_data.get('username')



                return redirect('/login/')

    context = {'form': form}
    return render(request, 'main/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')  # homepage
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')




def home(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']


    productsall = Product.objects.all()
    productswomen = Product.objects.filter(gender='WOMAN')
    context = {'products': productsall, 'productswomen': productswomen, 'cartItems': cartItems}
    return render(request, 'main/home.html', context)


def base(request):
    user = User.objects.all()
    return render(request, 'base_site.html', {'user': user})


def about(request):
    context = {}
    return render(request, 'main/about.html', {})


def details(request, product_id):
    #ERRORHANDLING!?
    productsall = Product.objects.all()
    product = get_object_or_404(Product, pk=product_id)

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    return render(request, 'main/details.html', {'products': productsall, 'product': product, 'cartItems': cartItems})



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
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    if order.shipping == True:
        #  Shipping  = first entry from Database
        #shippingcost= ShippingCost.objects.all()[:1].get()
        shippingcost= ShippingCost.objects.get(id=1)


        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM main_shippingcost")
        for id, service, costs in cursor:

            costsdec = Decimal(costs)
            shippingcost = round(costsdec, 2)
        cursor.close()


        totalwshipping = shippingcost + order.get_cart_total



    context = {'items': items, 'order': order,'cartItems':cartItems,
               'shippingcost': shippingcost, 'totalwshipping': totalwshipping}
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

