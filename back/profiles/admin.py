from django.contrib import admin
from .models import Address, Card_Detail, Customer_Profile
# Register your models here.

admin.site.register(Address)
admin.site.register(Card_Detail)
admin.site.register(Customer_Profile)
