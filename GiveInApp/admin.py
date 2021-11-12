from django.contrib import admin
from GiveInApp import models as m
# Register your models here.

admin.site.register(m.Category)
admin.site.register(m.Institution)
admin.site.register(m.Donation)

