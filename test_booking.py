#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarRental.settings')

# Add testserver to ALLOWED_HOSTS for testing
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from home.models import Booking, Car

# Check if car exists
car = Car.objects.filter(id=10).first()
print(f"Car ID 10 exists: {car is not None}")
if car:
    print(f"  Car: {car.brand} {car.name}")

# Create a test user
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
print(f"\nUser: {user.username} (created: {created})")
print(f"User has profile: {hasattr(user, 'profile')}")

# Login with the client
client = Client()
client.force_login(user)

# Set dates
pickup = (date.today() + timedelta(days=1)).isoformat()
return_date = (date.today() + timedelta(days=3)).isoformat()

print(f"\nDates:")
print(f"  Pickup: {pickup}")
print(f"  Return: {return_date}")

# Test booking
print(f"\nTesting POST to /car_rent/10/")
response = client.post('/car_rent/10/', {
    'pickup_date': pickup,
    'return_date': return_date
}, follow=True)

print(f"Status Code: {response.status_code}")
print(f"Redirect Chain: {response.redirect_chain}")

# Check if booking was created
bookings = Booking.objects.filter(user=user).order_by('-id')
print(f"\nBookings for user: {bookings.count()}")
for b in bookings[:3]:
    print(f"  - Booking {b.id}: {b.car.brand} {b.car.name} ({b.pickup_date} to {b.return_date})")
