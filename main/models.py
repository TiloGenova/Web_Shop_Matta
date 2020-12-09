#from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.

class Product(models.Model):

    CHOICESCAT = (
        ('tshirt', 'T-Shirt'),
        ('pullover', "Pullover"),
        ('dress', 'Dress'),
        ('socks', 'Socks'),
    )

    LABEL_CHOICE = (
        ('P', 'primary'),
        ('S', "secondary"),
        ('D', 'danger'),
    )

    SIZETYPES = models.TextChoices('Size', 'S S/M M M/L L')
    GENDER = models.TextChoices('Gender', 'WOMEN MEN')


    active = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    gender = models.CharField(choices=GENDER.choices, max_length=5)
    size = models.CharField(choices=SIZETYPES.choices, max_length=4)
    category = models.CharField(max_length=150, null=False, choices=CHOICESCAT)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=350)
    text = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    discount_price = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    image = models.ImageField(upload_to='media/')
    discount = models.BooleanField()
    label = models.CharField(max_length=1, choices=LABEL_CHOICE)
    new = models.BooleanField(default=False)
    digital = models.BooleanField(default=False, null=True, blank=True)
    url = models.URLField(blank=True)


    def __str__(self):
        return self.title

    @property #Errorhandling    in Case ther eis no image file
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.title

    @property
    def get_total(self):
        if self.product.discount_price > 0:
            total = self.product.discount_price*self.quantity
        else:
            total = self.product.price*self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    region = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address









