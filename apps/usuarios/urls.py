from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),  # Caminho para a view de registro
    path('password-reset/', views.password_reset_local, name='password_reset_local'),
]
