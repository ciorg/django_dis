from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .visualizer import Bitcoin

@login_required(login_url='/mylogin/login/')
def index(request):
    context = {}
    return render(request, 'crypto/index.html', context)

@login_required(login_url='/mylogin/login/')
def btc(request):
    script, div = Bitcoin().graph_data()
    context = {"script": script,
               "div": div}

    return render(request, 'crypto/btc.html', context)