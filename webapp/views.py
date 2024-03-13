from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт успешно создан!")
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
            messages.success(request, "Вы вошли в аккаунт!")
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/my_login.html', context=context)

@login_required(login_url='my_login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html', context=context)

@login_required(login_url='my_login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана!")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/create_record.html', context=context)


@login_required(login_url='my_login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно изменена!")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/update_record.html', context=context)

@login_required(login_url='my_login')
def singular_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'webapp/view_record.html', context=context)

@login_required(login_url='my_login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Запись успешно удалена!")
    return redirect("dashboard")

def user_logout(request):
    auth.logout(request)
    messages.success(request, "Вы вышли из аккаунта!")
    return redirect("my_login")

