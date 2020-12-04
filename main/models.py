#from __future__ import unicode_literals
from django.db import models
from django.conf import settings



# Create your models here.

class Product(models.Model):

    CHOICESCAT = (
        ('tshirt', 'T-Shirt'),
        ('pullover', "Pullover"),
        ('dress', 'Dress'),
        ('socks', 'Socks'),
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
    discountprice = models.DecimalField(decimal_places=2, max_digits=7, default=0.00, blank=True)
    image = models.ImageField(upload_to='portfolio/images/')
    discount = models.BooleanField()
    new = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

#User = settings.AUTH_USER_MODEL






'''class CartManager(models.Manager):
    def new_cart(self, user=None):
        return self.model.objects.create(user=user)


class Cart(models.Model):
    #user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)  # also for users without lockin
    products = models.ManyToManyField(Product, blank=True)  # blank=True  empty cart possible
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    #subtotal = models.DecimalField()
    #discount =
    objects = CartManager()

    def __str__(self):
        return self.id'''


