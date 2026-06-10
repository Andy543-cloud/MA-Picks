from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import date

# --- 1. USER PROFILE ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default_avatar.png')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

# --- 2. CAR MODEL (Define this BEFORE Order/Booking) ---
class Car(models.Model):
    TRANSMISSION_CHOICES = [('Auto', 'Automatic'), ('Manual', 'Manual')]
    
    name = models.CharField(max_length=100, default="Unknown Car")
    brand = models.CharField(max_length=50, default="Unknown")
    city = models.CharField(max_length=100, default="Accra", blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Auto')
    fuel_type = models.CharField(max_length=20, default="Petrol")
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# --- 3. ORDER MODEL ---
class Order(models.Model):
    # Using 'Car' as a string is fine, but since Car is now defined above, it works perfectly
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Add any other fields you need for Order here (e.g. status, date)
    
    def __str__(self):
        return f"Order: {self.car.name} by {self.user.username}"

# --- 4. BOOKING MODEL ---
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    license_number = models.CharField(max_length=50, blank=True, null=True)
    pickup_date = models.DateField()
    return_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    
    PAYMENT_CHOICES = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Failed', 'Failed')]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_days(self):
        if self.pickup_date and self.return_date:
            delta = self.return_date - self.pickup_date
            return max(delta.days, 1)
        return 0

    @property
    def total_rent(self):
        if self.car and self.total_days:
            return self.total_days * self.car.price_per_day
        return 0

# --- 5. CONTACT MESSAGES ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"