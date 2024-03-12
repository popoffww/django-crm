from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import *

def home(request):
    return render(request, 'webapp/index.html')

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()


            return redirect("my_login")

    context = {'form': form}

    return render(request, 'webapp/register.html', context=context)

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/my_login.html', context=context)

@login_required(login_url='my_login')
def dashboard(request):




    return render(request, 'webapp/dashboard.html')


def user_logout(request):

    auth.logout(request)


    return redirect("my_login")
