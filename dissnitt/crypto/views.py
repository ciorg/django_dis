from django.http import HttpResponse
from django.shortcuts import render

from .visualizer import Bitcoin

def index(request):
    context = {}
    return render(request, 'crypto/index.html', context)

def btc(request):
    script, div = Bitcoin().graph_data()
    context = {"script": script,
               "div": div}

    return render(request, 'crypto/btc.html', context)