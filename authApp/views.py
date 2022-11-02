from email import message
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, logout

from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
  
        
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            name = username
            return render(request, 'index.html', {'name': name})
        else:
            messages.error(request, 'Bad Credentials')
            return redirect('index')
    
    return render(request, 'login.html')


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # user validation
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try other username")
            return redirect('register')
                
        if User.objects.filter(email=email):
            messages.error(request, "Email already exist! Please try other email")
            return redirect('register')
            
        if len(username) > 20:
            messages.error(request, "Username must be under than 20 characters")    
            return redirect('register')
        
        if password1 != password2:
            messages.error(request, "Passwords didn't match")
            return redirect('register')
        
        if len(password1) or len(password2) > 8:
            messages.error(request, 'Password must have more than 8 characters')
            return redirect('register')
            
            
        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
               
        return redirect('login')
    
    return render(request, 'register.html')

def signout(request):
    logout(request)
    
    return redirect('index')