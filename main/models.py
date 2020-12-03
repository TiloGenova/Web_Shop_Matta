#from __future__ import unicode_literals
from django.db import models



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
    image = models.ImageField(upload_to='portfolio/images/')
    discount = models.BooleanField()
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title