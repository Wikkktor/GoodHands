import pytest
from django.contrib.auth.models import User
from GiveInApp.models import Category, Institution, Donation


@pytest.fixture
def login():
    return User.objects.create(username='test')