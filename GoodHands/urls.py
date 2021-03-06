"""GoodHands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from GiveInApp import views as v

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', v.MainPageView.as_view(), name='main_page'),
    path('accounts/login/', v.LoginView.as_view(), name='login'),
    path('accounts/register/', v.RegisterView.as_view(), name='register'),
    path('donation/', v.AddDonationView.as_view(), name='add_donation'),
    path('accounts/logout/', v.LogoutView.as_view(), name='logout'),
    path('thank-you/', v.DonationConfirmation.as_view(), name='thank_you'),
    path('profile/', v.ProfileView.as_view(), name='profile'),
    path('profiles/list', v.super_user_list_view, name='users_list'),
    path('profiles/create', v.add_user_view, name='users_create'),
    path('profiles/update/<int:pk>', v.Modify_user.as_view(), name='users_modify'),
    path('profiles/delete/<int:pk>', v.Delete_user.as_view(), name='users_delete')
]
