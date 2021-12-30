from django.urls import path, include

from .views import register, home, profile
app_name = "accounts"

urlpatterns = [
    path('', home, name="home"),
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
]