from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    first_line = models.CharField(max_length=256)
    post_code = models.CharField(max_length=50)
    # etc.
    primary = models.BooleanField(default=False)
    short_name = models.CharField(max_length=50)

    def __str__(self):
        return self.short_name
