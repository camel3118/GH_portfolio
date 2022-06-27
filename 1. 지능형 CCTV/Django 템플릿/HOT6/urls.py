"""streamProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Account.urls')),
    path('View/',include('View.urls')),
    path('Seoul/',include('CCTV1.urls')),
    path('KohSamui/',include('CCTV2.urls')),
    path('Davao/',include('CCTV3.urls')),
    path('FallingDown/',include('CCTV4.urls')),
    path('Fire/',include('CCTV5.urls')),
    path('Webcam/',include('CCTV6.urls')),
    path('Webcam2/',include('CCTV7.urls')),
]
