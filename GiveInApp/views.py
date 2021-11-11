from django.shortcuts import render

# Create your views here.
from django.views import View


class MainPageView(View):
    def get(self, request):
        context = render(request, 'index.html')
        return context


class LoginView(View):
    def get(self, request):
        context = render(request, 'login.html')
        return context


class RegisterView(View):
    def get(self, request):
        context = render(request, 'register.html')
        return context


class AddDonationView(View):
    def get(self, request):
        context = render(request, 'form.html')
        return context
