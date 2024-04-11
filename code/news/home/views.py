from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from .news import *


# News API
# 2e25cce3b0d0481aab616a68309b885c
# Create your views here.
def home(request):
    l = get_top_stories()
    return render(request,'home/home.html', {'articles': l["articles"]})

def logout_view(request):
    logout(request)
    return redirect('home')
