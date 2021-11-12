from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Institution(models.Model):
    CHOICES = [
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna')
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(default=1, choices=CHOICES, max_length=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name + " " + self.description


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quantity) + " " + self.institution.name
