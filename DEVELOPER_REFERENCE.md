# Developer's Quick Reference - Account Feature

## Quick Query Reference

### Get User's Profile Data
```python
from django.contrib.auth.models import User

# Get user from request
user = request.user
profile = user.profile

# Display user info
print(f"Name: {user.first_name} {user.last_name}")
print(f"Email: {user.email}")
print(f"Phone: {profile.phone}")
print(f"City: {profile.city}")
print(f"Member Since: {user.date_joined}")
```

### Check if User is Authenticated
```python
if request.user.is_authenticated:
    print(f"Hello {request.user.first_name}")
else:
    print("User is not logged in")
```

### Get All Users with Profiles
```python
from .models import UserProfile

profiles = UserProfile.objects.all()
for profile in profiles:
    print(f"{profile.user.username}: {profile.phone}, {profile.city}")
```

---

## Template Usage

### Show User Info in Template
```django
<!-- If user is logged in -->
{% if request.user.is_authenticated %}
    <p>Hello {{ request.user.first_name }} {{ request.user.last_name }}</p>
    <p>Email: {{ request.user.email }}</p>
    <p>Phone: {{ request.user.profile.phone }}</p>
    <p>City: {{ request.user.profile.city }}</p>
{% else %}
    <p>Please login to see your profile</p>
{% endif %}
```

### Show Join Date
```django
<p>Member Since: {{ request.user.date_joined|date:"M d, Y" }}</p>
```

### Show Profile Picture
```django
{% if request.user.profile.profile_picture %}
    <img src="{{ request.user.profile.profile_picture.url }}" alt="Profile">
{% else %}
    <img src="https://via.placeholder.com/50?text={{ request.user.first_name|first }}" alt="Profile">
{% endif %}
```

---

## View Protection

### Require Login
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='customer_login')
def my_protected_view(request):
    return render(request, 'my_template.html')
```

### Check Authorizations
```python
@login_required
def edit_profile(request):
    if request.user != requested_user:
        return HttpResponseForbidden("You cannot edit other users' profiles")
    # Continue with edit logic
```

---

## Model Customization

### Add Custom Fields to UserProfile
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Add new fields below:
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(max_length=20, default='en')
    
    def __str__(self):
        return f"{self.user.username} Profile"
```

Then run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Common Tasks

### Update User Profile
```python
def update_profile(request):
    profile = request.user.profile
    profile.phone = request.POST.get('phone')
    profile.city = request.POST.get('city')
    profile.save()
    
    user = request.user
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.save()
```

### Change User Password
```python
from django.contrib.auth import update_session_auth_hash

def change_password(request):
    user = request.user
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep user logged in
        return "Password changed successfully"
```

### Upload Profile Picture
```python
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES['picture']:
        request.user.profile.profile_picture = request.FILES['picture']
        request.user.profile.save()
        return "Picture uploaded"
```

---

## Form Examples

### Custom Signup Form
```python
from django import forms
from django.contrib.auth.models import User

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    city = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
```

### Use in View
```python
def register(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                city=form.cleaned_data['city']
            )
            return redirect('customer_login')
    else:
        form = CustomSignupForm()
    return render(request, 'register.html', {'form': form})
```

---

## Admin Customization

### Enhanced Admin Display
```python
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'phone', 'city', 'date_created')
    list_filter = ('city', 'date_created')
    search_fields = ('user__username', 'phone', 'city')
    readonly_fields = ('date_created',)
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
```

---

## URL Routing Tips

### Add Profile Edit URL
```python
# In urls.py
path('edit_profile/', views.edit_profile, name='edit_profile'),

# In views.py
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        # Handle form submission
        return redirect('customer_homepage')
    return render(request, 'edit_profile.html', {'profile': profile})
```

---

## Useful Django Template Tags

```django
<!-- Format date -->
{{ request.user.date_joined|date:"M d, Y" }}

<!-- Get first character -->
{{ request.user.first_name|first|upper }}

<!-- Default value if blank -->
{{ request.user.profile.phone|default:"Not Provided" }}

<!-- Truncate text -->
{{ request.user.profile.bio|truncatewords:10 }}

<!-- URL encoding -->
{{ profile.name|urlencode }}
```

---

## JavaScript Customization

### Add More Dropdown Functions
```javascript
// In customer_navbar.html
function toggleAccountDropdown(event) {
    event.preventDefault();
    event.stopPropagation();
    const dropdown = document.getElementById('accountDropdown');
    dropdown.classList.toggle('show');
}

// Add custom function
function closeAccountDropdown() {
    document.getElementById('accountDropdown').classList.remove('show');
}

// Update settings with AJAX
function updateUserEmail(newEmail) {
    fetch('/api/update-email/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: newEmail})
    }).then(res => res.json()).then(data => alert(data.message));
}
```

---

## Security Checklist

- [ ] All views that need auth have `@login_required` decorator
- [ ] All forms have `{% csrf_token %}`
- [ ] Passwords are hashed (Django does this automatically)
- [ ] User input is validated and sanitized
- [ ] Email addresses are stored as lowercase (add custom save method)
- [ ] No sensitive data in JavaScript
- [ ] Redirect after logout
- [ ] Permission checks for user actions

---

## Performance Tips

```python
# Use select_related for ForeignKey
user_profiles = UserProfile.objects.select_related('user').all()

# Use prefetch_related for ManyToMany
bookings = Booking.objects.prefetch_related('car').all()

# Cache frequently accessed data
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_user_stats(request):
    return render(request, 'stats.html')

# Use get_object_or_404 for safer queries
from django.shortcuts import get_object_or_404
user = get_object_or_404(User, username=username)
```

---

## Debugging Tips

### Check User Authentication
```python
print(f"Is authenticated: {request.user.is_authenticated}")
print(f"Is active: {request.user.is_active}")
print(f"Is staff: {request.user.is_staff}")
print(f"Is superuser: {request.user.is_superuser}")
```

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Profile not found | Check signal is registered, restart server |
| Avatar not showing | Check media directory exists, file permissions |
| Login redirects infinitely | Check LOGIN_URL in settings |
| CSRF token missing | Add `{% csrf_token %}` in form |
| Migrations fail | Delete db.sqlite3, run migrate from scratch |

---

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Authentication: https://docs.djangoproject.com/en/4.0/topics/auth/
- Models: https://docs.djangoproject.com/en/4.0/topics/db/models/
- Signals: https://docs.djangoproject.com/en/4.0/topics/signals/
- Security: https://docs.djangoproject.com/en/4.0/topics/security/

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: Active Development Ready
