import json
from . models import *

#to bundle  the functions for unregistered users
# to follow the D.R.Y. rules  -  not to repeat code

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

    print('Order2:', order)
    print('ITEM with stock:', items)


    return{'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        #query the parent object(order), the child object in all lower case  (orderitem)
        #  _set.all   > all the order items

    else:
        cookieData = cookieCart(request)   #function in utils.py
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']


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

