from django.contrib.auth.models import User
from django.forms import ModelForm


class UserForm(ModelForm):
    model = User
    fields = '__all__'
