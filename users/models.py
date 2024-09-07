from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

class Creator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Advertiser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Association(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
