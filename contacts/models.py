from django.db import models
from django.contrib.auth.models import AbstractUser

class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='contacts_auth_users')
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='contacts_auth_users')

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name