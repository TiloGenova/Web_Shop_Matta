from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


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

'''def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    print('New Cart created')
    return cart_obj


def cart(request):
    cart_id = request.session.get('cart_id', None)   # get the session
    qs = Cart.objects.filter(id=cart_id)  # if there is a session
    if qs.count() == 1:                    # test that it (one) exists
        cart_obj = qs.first()       # session (first)  is set to cart_obj
        cart_obj.save()
    else:
        cart_obj = Cart.objects.new(user=request.user)        #if no session exits or not just exactly one  a new session is created
        request.session['cart_id'] = cart_obj.id
    return render(request, 'cart.html', {})'''
