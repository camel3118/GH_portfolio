from django.shortcuts import render

# Create your views here.

def Dashboard(request):
    return render(request, 'View/Dashboard.html')

def ProjectOverview(request):
    return render(request, 'View/ProjectOverview.html')

def AgilePlannig(request):
    return render(request, 'View/Sprintplanning.html')

def Calendar(request):
    return render(request, 'View/Calendar.html')

def SystemArchitecture(request):
    return render(request, 'View/SystemArchitecture.html')

def GoogleMaps(request):
    return render(request, 'View/GoogleMaps.html')

def Profile(request):
    return render(request, 'View/Profile.html')