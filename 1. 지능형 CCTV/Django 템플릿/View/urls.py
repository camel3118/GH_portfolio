from django.urls import path
from .import views

urlpatterns = [
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('ProjectOverview/', views.ProjectOverview, name='ProjectOverview'),
    path('Sprintplanning/', views.AgilePlannig, name='Sprintplanning'),
    path('Calendar/', views.Calendar, name='Calendar'),
    path('SystemArchitecture/', views.SystemArchitecture, name='SystemArchitecture'),
    path('GoogleMaps/', views.GoogleMaps, name='GoogleMaps'),
    path('Profile/', views.Profile, name='Profile'),
]