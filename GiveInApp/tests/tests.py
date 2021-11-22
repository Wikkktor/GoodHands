import pytest
from django.urls import reverse
from django.test import Client


# Main Page Tests

@pytest.mark.django_db
def test_main_page_view_not_logged():
    client = Client()
    response = client.get(reverse('main_page'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_main_page_view_logged_in(login):
    client = Client()
    client.force_login(login)
    response = client.get(reverse('main_page'))
    assert response.status_code == 200




