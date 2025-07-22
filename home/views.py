# home/views.py
from django.shortcuts import render

def ViewHomepage(request):
    return render(
        request, 
        'home.html', 
        {
        'title': "Welcome to the Home Page!",
        }
    )