from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
