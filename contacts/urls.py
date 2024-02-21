"""
URL configuration for contacts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import contact_list, add_contact, contact_detail, update_contact, delete_contact, createAuthUser, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register', createAuthUser),
    path('auth/login', login),
    path('contacts/list', contact_list),
    path('contacts/<int:id>', contact_detail),
    path('contacts/update/<int:id>', update_contact),
    path('contacts/delete/<int:id>', delete_contact),
    path('contacts/add', add_contact),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
