from django.urls import path
from .import views

urlpatterns = [
    path('', views.login, name='Login'),
    path('Signup/', views.signup, name='Signup'),
    path('Logout/', views.logout, name='Logout'),
]
