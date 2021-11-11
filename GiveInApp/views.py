from django.shortcuts import render

# Create your views here.
from django.views import View
from django.db.models import Sum
from GiveInApp.models import Institution, Donation


class MainPageView(View):
    def get(self, request):
        institutions = len(Institution.objects.all())
        donations = Donation.objects.aggregate(Sum('quantity'))
        context = render(request, 'base.html', {'institutions': institutions, 'donations': donations['quantity__sum']})
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
