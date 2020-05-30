from colorfield.fields import ColorField
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    colors = models.ManyToManyField('Color')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, blank=False)
    rgb = ColorField(default='#000000')

    def __str__(self):
        return self.name


class SpecialOffer(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    products = models.ManyToManyField(Product, related_name='special_offers')

    def get_products(self):
        return self.products.all().order_by('name')

    def __str__(self):
        return self.name
