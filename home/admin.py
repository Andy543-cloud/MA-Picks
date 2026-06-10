from django.contrib import admin
from .models import Car, Booking, UserProfile
# booking/admin.py
from django.contrib import admin




admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(UserProfile)
