# User Account Logo & Info Tab Feature - Setup Guide

## Overview
This feature adds a user account dropdown menu in the top-right corner of the navbar. After signup/login, users will see their profile picture/avatar and can click to view their complete account information.

## What Was Implemented

### 1. **Database Model Changes**
- **UserProfile Model**: New model created to store additional user information
  - `user` - Link to Django User model
  - `phone` - User's contact number
  - `city` - User's location
  - `profile_picture` - User's avatar/profile photo
  - `date_created` - Account creation timestamp

### 2. **Authentication Views**
Updated `home/views.py` with:
- `customer_signup()` - Handles user registration with validation
- `customer_login()` - Authenticates users and creates session
- `customer_homepage()` - Protected view for logged-in users
- `signout()` - Logs out users safely

### 3. **User Interface Updates**

#### Navbar Account Dropdown (`customer_navbar.html`)
The navbar now displays:
- **For Logged-Out Users**: "Login" and "Sign Up" buttons
- **For Logged-In Users**: Account menu with:
  - Profile picture (avatar)
  - User's full name and email
  - User profile information:
    - Username
    - Phone number
    - City
    - Member since date
  - Quick action buttons:
    - My Profile
    - Settings
    - My Bookings
    - Logout

#### Authentication Pages
- **Signup Form** (`customer_signup.html`): Collects first name, last name, username, email, phone, city, password
- **Login Form** (`customer_login.html`): Username and password with "Remember me" option

### 4. **URL Routes** (`home/urls.py`)
Enabled the following routes:
- `/customer_signup/` - User registration
- `/customer_login/` - User login
- `/customer_homepage/` - Dashboard for logged-in users
- `/signout/` - Logout functionality

### 5. **Styling & Interactivity**
Added CSS for:
- Account dropdown menu styling
- Smooth animations and hover effects
- Responsive design
- Color-coded menu items
- Avatar styling with border

## Features

### Account Dropdown Menu
✅ Click on user's avatar to toggle dropdown
✅ Shows all user information clearly
✅ Member since date displayed
✅ Phone and city information visible
✅ Quick navigation links
✅ Auto-close when clicking outside
✅ Responsive on mobile devices

### User Authentication
✅ Email uniqueness validation
✅ Username uniqueness validation
✅ Password confirmation matching
✅ Auto-create UserProfile with every signup
✅ Secure login with Django authentication
✅ Session management

### Security Features
✅ CSRF protection on all forms
✅ Password hashing
✅ Login required decorators on protected views
✅ Automatic profile creation signals

## Setup Instructions

### 1. Generate Placeholder Avatar
The system uses placeholder avatars if no profile picture is uploaded. To add custom avatars:

```bash
# Create the profiles upload directory if it doesn't exist
mkdir -p media/profiles/
```

### 2. Run Migrations (Already Done)
Migrations have already been created and applied:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Already Done)
Admin account created:
- Username: `admin`
- Email: `admin@example.com`
- You can set password when first logging in

### 4. Access Admin Panel
Visit: `http://localhost:8000/admin/`
- Manage UserProfiles
- View user registrations
- Edit user information

## Testing the Feature

### 1. **Test Signup**
```
1. Visit http://localhost:8000/customer_signup/
2. Fill in all required fields
3. Click "Create Account"
4. You'll be redirected to login page
```

### 2. **Test Login**
```
1. Visit http://localhost:8000/customer_login/
2. Enter username and password
3. Click "Login"
4. You'll be redirected to customer homepage
```

### 3. **Test Account Dropdown**
```
1. After login, look at top-right corner
2. You'll see a circular avatar with your initial
3. Click the avatar to open dropdown menu
4. See all your information displayed
5. Click outside to close the dropdown
```

### 4. **Test Logout**
```
1. Click avatar in top-right
2. Click "Logout" in dropdown
3. You'll be logged out and redirected
```

## User Flow

```
Anonymous User
    ↓
    ├─→ Click "Sign Up" button
    │   ├─→ Fill signup form
    │   ├─→ Create account
    │   └─→ Redirect to login
    │
    └─→ Click "Login" button
        ├─→ Enter credentials
        ├─→ Login successful
        └─→ See account avatar in navbar
            └─→ Click avatar
                └─→ View account dropdown with all info
                    ├─→ View profile
                    ├─→ Access settings
                    ├─→ View bookings
                    └─→ Logout
```

## Files Modified

1. **home/models.py**
   - Added UserProfile model
   - Added signal handlers for auto-profile creation

2. **home/views.py**
   - Added authentication views (signup, login, logout)
   - Added user homepage view
   - Added login_required decorators

3. **home/urls.py**
   - Enabled authentication routes
   - Linked views to URLs

4. **home/templates/customer_navbar.html**
   - Added account dropdown HTML
   - Added dropdown CSS and styling
   - Added JavaScript for dropdown toggle functionality

5. **home/templates/customer_signup.html**
   - Updated form action and method
   - Added better styling
   - Added validation messages

6. **home/templates/customer_login.html**
   - Updated form action and method
   - Added better styling
   - Added validation messages

7. **home/admin.py**
   - Registered UserProfile model in Django admin

## Customization Options

### Change Avatar Placeholder Style
Edit the placeholder URL in `customer_navbar.html`:
```html
<img src="https://via.placeholder.com/40?text=YOUR_CUSTOM_TEXT" ...>
```

### Change Colors
Edit the CSS in `customer_navbar.html`:
```css
.account-avatar {
    border: 2px solid #71cc09; /* Change border color */
}
```

### Add More User Fields
Edit `UserProfile` model in `models.py`:
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Add your custom fields here
    department = models.CharField(max_length=100, blank=True, null=True)
```
Then run migrations.

## Troubleshooting

### Issue: "UserProfile matching query does not exist"
**Solution**: Run migrations and restart server
```bash
python manage.py migrate
python manage.py runserver
```

### Issue: Login redirects to signup
**Solution**: Check that credentials are correct and user exists in database
```bash
python manage.py shell
from django.contrib.auth.models import User
User.objects.all()  # List all users
```

### Issue: Avatar not showing
**Solution**: System uses placeholder images if no profile_picture is set. Upload an image in admin panel.

## Next Steps (Optional Enhancements)

1. **Profile Edit Page** - Allow users to update their information
2. **Profile Picture Upload** - Add image upload in profile settings
3. **Password Change** - Implement password reset functionality
4. **Email Verification** - Verify email during signup
5. **Social Login** - Add Google/Facebook login
6. **Two-Factor Authentication** - Add 2FA for security
7. **User Dashboard** - Create comprehensive user dashboard
8. **Notifications** - Add booking confirmations and updates

## Support

For issues or questions, check Django authentication documentation:
- https://docs.djangoproject.com/en/4.0/topics/auth/

---

**Setup Status**: ✅ Complete
**Feature Status**: ✅ Ready for Testing
**Database**: ✅ Migrated
**Admin Panel**: ✅ Configured
