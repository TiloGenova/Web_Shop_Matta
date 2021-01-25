from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .forms import CreateUserForm, Contactformmail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import cookieCart, cartData, guestOrder
import sqlite3
from decimal import Decimal
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.db import connection



# Create your views here.
def contactmail(request):
    if request.method == 'GET':
        form = Contactformmail()

    return render(request, 'main/contact.html', {'form': form})




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


global zerostock2
zerostock2 = []

def home(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    productsall = Product.objects.all()
    dataCart = cookieCart(request) #function in utils.py
    zerostock = dataCart['zerostock']
    y = zerostock2


    print('ZEROSTOCK2 from HOME:', y)


    context = {'products': productsall,'cartItems': cartItems, 'zerostock': zerostock,'zerostock2': zerostock2}
    return render(request, 'main/home.html', context)


def base(request):
    user = User.objects.all()
    return render(request, 'base_site.html', {'user': user})


def contact(request):
    #ERRORHANDLING!?
    productsall = Product.objects.all()


    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']

    return render(request, 'main/contact.html', {'products': productsall, 'cartItems': cartItems})



def about(request):
    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'main/about.html', context)


def cookiePolicy(request):
    return render(request, 'main/cookie_policy.html', {})


def privacyPolicy(request):
    return render(request, 'main/privacy_policy.html', {})
    #websitepolicies  kingnapalm  word:YFtD0jo3


def details(request, product_id):
    #ERRORHANDLING!?
    productsall = Product.objects.all()
    product = get_object_or_404(Product, pk=product_id)

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']

    dataCart = cookieCart(request) #function in utils.py
    zerostock = dataCart['zerostock']



    return render(request, 'main/details.html', {'products': productsall,
                                                 'product': product, 'cartItems': cartItems,
                                                 'zerostock': zerostock,'zerostock2': zerostock2})



def cart(request):

    productsall = Product.objects.all()
    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    dataCart = cookieCart(request) #function in utils.py
    zerostock = dataCart['zerostock']
    print('ZEROSTOCK from CART:', zerostock)


    context = {'products': productsall,'items': items, 'order': order,'cartItems':cartItems, 'zerostock': zerostock,'zerostock2': zerostock2}
    return render(request, 'main/cart.html', context)





def checkout(request):

    data = cartData(request)   #function in utils.py
    cartItems = data['cartItems']
    #global order
    order = data['order']
    items = data['items']
    shippingcost = 0
    global totalwshipping
    totalwshipping = 0


    print('ORDER def checkout:', order)
    print(type(order))

    global ordernumber
    if request.user.is_authenticated:
        ordernumber = getattr(order, 'id')
        print('Got closed order - ordernumber as INT:', ordernumber)
        print(type(ordernumber))



    #shipping = order.shipping
    #print('shipping:', shipping)

    if request.user.is_authenticated:
        if order.shipping == True:  #user logged in



            db = sqlite3.connect('db.sqlite3')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM main_shippingcost")
            for id, service, costs in cursor:

                costsdec = Decimal(costs)
                shippingcost = round(costsdec, 2)
            cursor.close()

            gct = order.get_cart_total
            #totalwshipping = shippingcost + order.get_cart_total

            totalwshipping = shippingcost + gct
            print('totalwshipping from checkout LOGGED IN:', totalwshipping)
        else:
            shippingcost = [0]


    else:

        if (order['shipping']) == True: #user NOT logged in
            try:
                db = sqlite3.connect('db.sqlite3')
                cursor = db.cursor()
                cursor.execute("SELECT * FROM main_shippingcost")
                for id, service, costs in cursor:

                    costsdec = Decimal(costs)
                    shippingcost = round(costsdec, 2)
                cursor.close()
                db.close()

            except:
                shippingcost =float(0.00)

            gct = (order['get_cart_total'])
            #totalwshipping = shippingcost + order.get_cart_total
            #global totalwshipping
            totalwshipping = shippingcost + gct
            print('totalwshipping from checkout NOT LOGGED IN:', totalwshipping)
        else:
            shippingcost = 0




    context = {'items': items, 'order': order,'cartItems':cartItems,
               'shippingcost': shippingcost, 'totalwshipping': totalwshipping}
    return render(request, 'main/checkout.html', context)






zerostockloggedin = []


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

    #BLOCK FOR ZEROSTOCK
    stock = getattr(product, 'stock')
    orderItem.zerostock = stock - orderItem.quantity
    print('Got STOCK - STOCK as INT:', stock)
    print(type(stock))
    print('Difference Stock and Cart:', orderItem.zerostock)
    productident = getattr(product, 'id')


    #ORIGINAL BLOCK
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()



    #CREATING ZEROSTOCK-LIST TO DISABLE BUTTONS FOR LOGGED IN USERS:
    global zerostock2
    if orderItem.zerostock <= 0:
        zerostock2.append(productident)

    elif orderItem.zerostock != 0:
        try:
            zerostock2.remove(productident)
        except ValueError:
            print('already removed from list')

    else:
        pass

    print('ZEROSTOCK_logged in:', zerostock2)



    return JsonResponse('Item was added YEAH', safe=False)  #  just to return a message   no template




from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):

    #totalwshipping = 0

    #print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    #print('verfuegbare Angaben checkout:', data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer, order = guestOrder(request, data)


    #GETTING THE TOTAL PRICE

    # Following block for logged in and not logged in users
    total = float(data['form']['total'])
    totaldec = Decimal(total)
    total = round(totaldec, 2)

    #print('TOTAL FLOAT processOrder:', total)
    print('TOTALwshipping:', totalwshipping)   # NOT DEFINED ????? 
    order.transaction_id = transaction_id
    print('ORDER ORDER ORDER:', order)
    print(type(order))
    orderint = getattr(order, 'id')
    print('ORDER ORDER ORDER INT:', orderint)
    print(type(orderint))



                # if total == order.get_cart_total:  =  without shippingcosts
    if total == totalwshipping:
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



    # reduction of stock after order:

    orderdict = {}
    data = cartData(request)   #function in utils.py
    order = data['order']
    #ordernumber = getattr(order, 'id')  #NEW and EMPTY ORDERNUMBER (CART WITHOUT PRODUCTS)


    # getting ordernumber as integer - finally getattr() did the job
    '''o = Order.objects.last()
    o = Order.objects.values('id')  #query set with all order IDs
    ordernum =Order.objects.values_list('id', flat=True)
    field_name = 'id'
    obj = Order.objects.last()  # LAST - POTENTIAL OVERLAP WITH NEW ORDER / OTHER CUSTOMER!?
    field_object = Order._meta.get_field(field_name)
    o2 = field_object.value_from_object(obj)'''


    #connecting to database and get the products and quantity for an order
    #__________Cursor to get PRODCUT AND QUANTITY:

    if request.user.is_authenticated:

        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()


        cursor.execute("SELECT product_id, quantity FROM main_orderitem WHERE order_id= ?", (ordernumber,))

        '''for row in cursor:
            print(row)
            product = row[0]
            quanity = row[1]
            print('prodID:', product)
            print('prodQ:', quanity)
            print('-----')'''


        for product_id, quanity in cursor:
            product_id = product_id
            print('prodID:', product_id)
            print('prodQ:', quanity)
            print('-----')

            #creating Dictionary
            orderdict[product_id] = quanity


        print('Order dict:', orderdict)
        print('##################################################')



        #Getting the stock values for the products

        #list of dict keys (product IDs):
        stockdict = {}
        x = orderdict.keys()
        print(x)

        for prodid in x:
            cursor.execute("SELECT stock FROM main_product WHERE id= ?", (prodid,))
            print(prodid)
            for stock in cursor:
                print('stock:', stock)

                stockdict[prodid] = stock

            print('-----')

        print('STOCK DICT:', stockdict)
        print('ORDER DICT:', orderdict)
        print('*****************')



        #Calculating the new stock values of the products

        # for key in orderdictionary:
        for item in x:
            stockoldtup = stockdict.get(item)
            stockold = stockoldtup[0]
            orderquantity = orderdict.get(item)

            print('stockold:', stockold)
            print('orderquantity:', orderquantity)

            stocknew = stockold - orderquantity
            print('New Stock:', stocknew)
            print('*****************')


        #Updating the stock values for the products

            update_cursor = db.cursor()
            update_cursor.execute("UPDATE main_product SET stock = ? WHERE main_product.id = ? ", (stocknew, item))
            db.commit()
        db.close()




    else:
        db = sqlite3.connect('db.sqlite3')
        cursor = db.cursor()

        cookieData = cookieCart(request)
        items = cookieData['items']

        print('ITEMS from !!!!!!!!!! STOCK UPDATE:', items)

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            product_id = int(item['product']['id'])
            quantity = int(item['quantity'])

            print('product:', product)
            print('product_id:', product_id)
            print(type(product_id))
            print('quantity:', quantity)
            print(type(quantity))
            print('<<<<<<<<<<<<<<<')

            #creating Dictionary
            orderdict[product_id] = quantity


        print('Order dict:', orderdict)
        print('##################################################')

        #Getting the stock values for the products

        #list of dict keys (product IDs):
        stockdict = {}
        x = orderdict.keys()
        print(x)

        for prodid in x:
            cursor.execute("SELECT stock FROM main_product WHERE id= ?", (prodid,))
            print(prodid)
            for stock in cursor:
                print('stock:', stock)

                stockdict[prodid] = stock

            print('-----')

        print('STOCK DICT:', stockdict)
        print('ORDER DICT:', orderdict)
        print('*****************')


        #Calculating the new stock values of the products

        # for key in orderdictionary:
        for item in x:
            stockoldtup = stockdict.get(item)
            stockold = stockoldtup[0]
            orderquantity = orderdict.get(item)

            print('stockold:', stockold)
            print('orderquantity:', orderquantity)

            stocknew = stockold - orderquantity
            print('New Stock:', stocknew)
            print('*****************')


            #Updating the stock values for the products

            update_cursor = db.cursor()
            update_cursor.execute("UPDATE main_product SET stock = ? WHERE main_product.id = ? ", (stocknew, item))
            db.commit()
        db.close()



    # SENDING CONFIRMATION EMAIL
    #necessary settings Google mail account:
    #https://myaccount.google.com/lesssecureapps
    #https://accounts.google.com/b/0/DisplayUnlockCaptcha

    db = sqlite3.connect('db.sqlite3')
    cursor = db.cursor()

    cursor.execute("SELECT customer_id FROM main_order WHERE id= ?", (orderint,))
    customer_id = cursor.fetchone()
    print('CUSTOMERID:', customer_id)
    customer = customer_id[0]

    cursor.execute("SELECT name FROM main_customer WHERE id= ?", (customer,))
    customertup = cursor.fetchone()
    print('CUSTOMERNAME:', customer)
    nameanony = customertup[0]

    cursor.execute("SELECT email FROM main_customer WHERE id= ?", (customer,))
    emailtup = cursor.fetchone()
    print('CUSTOMEREMAIL:', emailtup)
    emailanony = emailtup[0]

    cursor.execute("SELECT address FROM main_shippingaddress WHERE order_id= ?", (orderint,))
    addresstup = cursor.fetchone()
    print('ADDRESSE:', addresstup)
    address = addresstup[0]

    cursor.execute("SELECT zipcode FROM main_shippingaddress WHERE order_id= ?", (orderint,))
    ziptup = cursor.fetchone()
    print('ZIP:', ziptup)
    zip = ziptup[0]

    cursor.execute("SELECT city FROM main_shippingaddress WHERE order_id= ?", (orderint,))
    citytup = cursor.fetchone()
    print('CITY:', citytup)
    city = citytup[0]

    cursor.execute("SELECT state FROM main_shippingaddress WHERE order_id= ?", (orderint,))
    statetup = cursor.fetchone()
    print('STATE:', statetup)
    state = statetup[0]

    cursor.execute("SELECT country FROM main_shippingaddress WHERE order_id= ?", (orderint,))
    countrytup = cursor.fetchone()
    print('COUNTRY:', countrytup)
    country = countrytup[0]





    cursor.execute("SELECT product_id, quantity FROM main_orderitem WHERE order_id= ?", (orderint,))
    orderitems = cursor.fetchall()
    print('ITEMSITEMSITEMS:', orderitems)

    productdict = {}
    for orderitem in orderitems:
        cursor.execute("SELECT title FROM main_product WHERE id= ?", (orderitem[0],))
        for producttitle in cursor:
            print(producttitle)

        productdict[producttitle] = orderitem
    print(productdict)

    z = 0
    alltextmail =''
    linemail = 'Articolo-ID: {}   Articolo: {}    Quantità: {}  \n'
    for item in productdict:
        title = list(productdict.keys())[z]
        print('TITLE:', title)
        print(type(title))
        values = list(productdict.values())[z]
        print('VALUES ID/QUANTITY:', values)
        print(type(values))

        a=linemail.format(values[0], title[0], values[1])
        print(a)
        alltextmail += a
        z += 1

    print(alltextmail)


    db.close()



    if request.user.is_anonymous:
        name = nameanony
        email = emailanony
        shipname = nameanony
    else:
        name = request.user.first_name
        email = request.user.email
        shipname = request.user.first_name +' '+ request.user.last_name


    context = {
        'customer': name,
        'order': orderint,
        'items': alltextmail,
        'shipping_name': shipname,
        'shipping_address': address,
        'shipping_zip': zip,
        'shipping_city': city,
        'shipping_state': state,
        'shipping_country': country,

    }
    template = render_to_string('main/email_confirmation.html', context)

    email = EmailMessage(
        'Il tuo ORDINE / MAGLIAMATTA', #Subject
        template,
        settings.EMAIL_HOST_USER,
        [email], # Receiver
        ['kingnapalm68@gmail.com', 'martam.colombo@gmail.com'],  # BCC

    )
    email.send(fail_silently=False)
    
    return JsonResponse('Payment complete!', safe=False)

