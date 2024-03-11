from django.shortcuts import render, redirect
from .forms import *

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.valid():
            form.save()
        # return redirect('')

    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)
