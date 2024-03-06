# from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    """Model for eshop items"""
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    size = models.CharField(max_length=15)

SIZE_CHOICES = [
        ("S", "S"),
        ("XS", "XS"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("X", "X")
    ]

class Order(models.Model):

    DESCRIPTION_CHOICES = []

    PAYMENT_CHOICES = [(1, "Paypal"), (2, "Card"), (3, "Apple")]

    item = models.CharField(max_length=100,
                            # choices=[(item, item) for item in Item.objects.values_list('item', flat=True).distinct().order_by('item')],
                            default="")
    description = models.CharField(max_length=100,
                            # choices=[(descr, descr) for descr in Item.objects.values_list('description', flat=True).distinct().order_by('description')],
                            default="")
    size = models.CharField(max_length=100,
                            choices=SIZE_CHOICES,
                            default="S")
    number = models.IntegerField()
    address = models.TextField()
    payment = models.IntegerField(choices=PAYMENT_CHOICES,
                               default=1)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.description.lower()} {self.item.lower()} of size {self.size}."