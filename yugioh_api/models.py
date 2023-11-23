from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    """
    using User class as a one to one field as recommended in:
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField()
    authenticated = models.BooleanField()
    token = models.CharField(max_length=32)
