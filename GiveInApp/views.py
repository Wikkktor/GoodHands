from django.contrib.messages.context_processors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Sum
from GiveInApp.models import Institution, Donation


class MainPageView(View):
    def get(self, request):
        institutions_amount = len(Institution.objects.all())
        foundation = Institution.objects.filter(type=1)
        non_gov_organization = Institution.objects.filter(type=2)
        local_collection = Institution.objects.filter(type=3)
        donations = Donation.objects.aggregate(Sum('quantity'))
        data = {'institutions': institutions_amount, 'donations': donations['quantity__sum'], 'foundations': foundation,
                'non_gov_organizations': non_gov_organization, 'local_collections': local_collection}
        context = render(request, 'base.html', data)
        return context


class LoginView(View):
    def get(self, request):
        context = render(request, 'login.html')
        return context


class RegisterView(View):
    def get(self, request):
        context = render(request, 'register.html')
        return context

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            User.objects.create(first_name=name, last_name=surname, email=email, username=email, password=password)
            return redirect('main_page')
        else:
            return HttpResponse('hasła nie są takie same')



class AddDonationView(View):
    def get(self, request):
        context = render(request, 'form.html')
        return context
