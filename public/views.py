from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html', {})


# сделать для авторизованных
@login_required(login_url="/admin")
def orders(request):
    return render(request, 'orders.html', {})


def sign_out(request):
    logout(request)
    return HttpResponse('Вы вышли')
