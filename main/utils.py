from django.shortcuts import render, get_object_or_404, redirect
import json
from . models import *

#to bundle  the functions for unregistered users
# to follow the D.R.Y. rules  -  not to repeat code


'''#outsource the quantity check  when Cart button is pushed
def quantityCheck(request):

    cartq = json.loads(request.COOKIES['cart'])  # json.loads  to parse it and to turn it back into a python dict
    print('Cart from quantityCheck:', cartq)

    return{'cartq': cartq}'''



def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])  # json.loads  to parse it and to turn it back into a python dict
    except:
        cart = {}

    print('Cart:', cart)
    items = []   # if user is not logged in
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']
    print('Order:', order)


    #CART CHECK PRODUCTCOUNT
    cartdict = cart
    zerostock = []
    #x = 0
    if request.user.is_anonymous:
        for item in cartdict:
            #print('###########')
            #print('ITEM ID from cartdict:', item)
            #print(type(item))

            quantdict = cartdict.get(item) #to get quantity of product in cart
            #print('quantdict:', quantdict) #still a dictonary
            countincart = quantdict.get('quantity') #getting the value for key 'quantity' from dictionary
            #print('Count from quantdict:', countincart)
            #print('###########')

            item = int(item)
            print('############################')
            print('ADDED new Item/Product.id:', item)
            #print(type(item))
            product = get_object_or_404(Product, pk=item)
            #product = Product.objects.get(id=item['product']['id'])
            #print('Prod  from  CARTCHECK DB:', product)
            #print(type(product))

            stock = getattr(product, 'stock')
            print('Got STOCK - STOCK as INT:', stock)
            #print(type(stock))

            #Block not needed - item can be used
            #productid = getattr(product, 'id')
            #print('ProdID  from  CARTCHECK DB:', productid)
            #print(type(productid))


            #DIFFERENCE BETWEEN STOCK AND AMOUNT IN CART
            x = stock - countincart
            print('Difference Stock and Cart:', x)
            #orderquantity = orderdict.get(item)

            if x <= 0:
                zerostock.append(item)

            else:
                pass

            print('LIST zerostock for template:', zerostock)
            print('############################')




    for i in cart:   # sum of items to show in cart
        try:    #Errorhandling  / In case there is no valid product in database

            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)


            #total = (product.price * cart[i]['quantity'])
            if product.discount_price > 0:
                total = (product.discount_price * cart[i]['quantity'])
            else:
                total = (product.price * cart[i]['quantity'])


            order['get_cart_total'] += total

            order['get_cart_items'] += cart[i]['quantity']


            item = {
                'product':{
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    'size': product.size,
                    'discount_price': product.discount_price,


                },
                'quantity': cart[i]["quantity"],
                'stock': product.stock,
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass

    #print('Order2:', order)
    #print('ITEMS with stock from cookieCart:', items)


    return{'cartItems': cartItems, 'order': order, 'items': items, 'zerostock': zerostock }


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        print('ITEMS FROM cartData:', items)
        print(type(items))

        cartItems = order.get_cart_items
        print('cartItems FROM cartData:', cartItems)
        print(type(cartItems))
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        cookieData = cookieCart(request)   #function in utils.py
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    #print('ITEM with stock from cartData:', items)

    return {'cartItems': cartItems, 'order': order, 'items': items}



def guestOrder(request, data):

    print('User is not logged in...')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()


    order = Order.objects.create(
        customer=customer,
        complete=False,
    )


    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order


