from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # Django'nun hazır auth URL'lerini dahil ediyoruz (login, logout, password reset vs.)
    path("", include("django.contrib.auth.urls")),
    
    # Kendi ekleyeceğimiz URL'ler
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]

