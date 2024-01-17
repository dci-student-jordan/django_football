from django.db import models

# Create your models here.


class Item(models.Model):
    """Model for eshop items"""
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    size = models.CharField(max_length=15)