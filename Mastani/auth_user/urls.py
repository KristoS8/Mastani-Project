from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('role_based_redirect/', views.role_based_redirect, name='role_based_redirect'),
]