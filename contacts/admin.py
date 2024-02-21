from django.contrib import admin
from .models import Contact, AuthUser

admin.site.register(Contact)
admin.site.register(AuthUser)