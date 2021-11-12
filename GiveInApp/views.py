from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Sum
from GiveInApp.models import Institution, Donation, Category


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

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return redirect("register")


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
            user = User.objects.create(first_name=name, last_name=surname, email=email, username=email, password=password)
            user.set_password(password)
            user.save()
            return redirect('main_page')
        else:
            return HttpResponse('hasła nie są takie same')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main_page')


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = render(request, 'form.html', {'category': categories, 'institutions': institutions})
        return context
