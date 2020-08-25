from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from account.forms import UserForm

# Create your views here.

def register(request):
    '''
    Register a new user
    '''
    template = 'account/register.html'
    if request.method == 'GET':
        return render(request, template, {'userForm':UserForm()})
    
    #POST
    userForm = UserForm(request.POST)
    if not userForm.is_valid():
        return render(request, template, {'userForm':userForm})
    
    userForm.save()
    messages.success(request, 'Thank you for register!')
    return redirect('main:main')

def login(request):
    '''
    Login as existing user
    ''' 
    template = 'account/login.html'
    if request.method == 'GET':
        return render(request, template)
    
    #POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        messages.error(request, 'Please complete required information')
        return render(request, template)
    
    user = authenticate(username=username, password=password)
    if not user:    #authentication fails
        messages.error(request, 'Login Failure')
        return render(request, template)
    
    #login success
    auth_login(request, user)
    messages.success(request, 'Welcome Back')
    return redirect('main:main')

def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, 'See You Next Time')
    return redirect('main:main')
    
    