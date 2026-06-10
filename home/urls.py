from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("services/", views.service, name="service"),
    path("faq/", views.faq, name="faq"),
    path("cars/", views.cars, name="cars"),
    path("search/", views.search_results, name="search_results"),
    
    # Matching the cleaned views names:
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("customer_logout/", views.signout, name="signout"),
    path("customer_homepage/", views.customer_homepage, name="customer_homepage"),
    
    # Car Rental & Orders
    path("order_details/<int:order_id>/", views.order_details, name="order_details"),
    path("car_rent/<int:car_id>/", views.car_rent, name="car_rent"),
    path("past_orders/", views.past_orders, name="past_orders"),

    
    # Utilities
    path("contact/", views.contact_us, name="contact_us"),
    path("generate_ppt/", views.generate_ma_picks_ppt, name="generate_ppt"),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)