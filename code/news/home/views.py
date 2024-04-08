from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def logout_view(request):
    logout(request)
    return redirect('home')
