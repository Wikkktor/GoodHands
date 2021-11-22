from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.utils.decorators import method_decorator
from GiveInApp.models import Institution, Donation, Category


class MainPageView(View):
    """
    Main page View

    """
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
    """
    User login view
    """
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
    """
    User registration view
    """
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
            user = User.objects.create(first_name=name, last_name=surname, email=email, username=email,
                                       password=password)
            user.set_password(password)
            user.save()
            return redirect('main_page')
        else:
            return HttpResponse('hasła nie są takie same')


class LogoutView(View):
    """
    User logout View
    """
    def get(self, request):
        logout(request)
        return redirect('main_page')


class AddDonationView(LoginRequiredMixin, View):
    """
    Adding donation view
    """
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = render(request, 'form.html', {'category': categories, 'institutions': institutions})
        return context

    def post(self, request):
        d = Donation.objects.create(quantity=request.POST['bags'], institution_id=request.POST['organization'],
                                    address=request.POST['address'], city=request.POST['city'],
                                    zip_code=request.POST['postcode'], phone_number=request.POST['phone'],
                                    pick_up_time=request.POST['time'], pick_up_date=request.POST['data'],
                                    pick_up_comment=request.POST['more_info'])
        ids = request.POST.getlist('categories')
        c = Category.objects.filter(id__in=ids)
        d.categories.set(c)
        return redirect('thank_you')


class DonationConfirmation(View):
    """
    Success donation, thank you page
    """
    def get(self, request):
        return render(request, 'form-confirmation.html')


class ProfileView(LoginRequiredMixin, View):
    """
    User profile view
    """
    def get(self, request):
        donation = {'donation': Donation.objects.all().sorted('pick_up_date')}
        return render(request, 'profile.html', donation)


@user_passes_test(lambda u: u.is_superuser)
def super_user_list_view(request):
    """
    List of users for superuser
    :param request:
    :return: list of users
    """
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@permission_required('is_superuser')
def add_user_view(request):
    """
    Adding new user as superuser
    :param request:
    :return: new user
    """
    if request.method == 'GET':
        return render(request, 'create_user.html')
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user = User()
            user.email = request.POST['email']
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            password = request.POST['password']
            user.username = request.POST['email']
            if bool(int(request.POST['superuser'])):
                user.is_superuser = True
            user.set_password(password)
            user.save()
            return redirect('users_list')


@method_decorator(permission_required('is_superuser'), name='dispatch')
class Modify_user(UpdateView):
    """
    Updating user
    """
    model = User
    template_name = 'update.html'
    fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_superuser')
    success_url = '/'


@method_decorator(permission_required('is_superuser'), name='dispatch')
class Delete_user(DeleteView):
    """
    deleting user
    """
    model = User
    template_name = 'update.html'
    success_url = '/'

