from collections import namedtuple
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calcs import CalcClass
from .forms import TimeForm
from .visualizer import GraphClass
from .models import Bitcoin, Etherium

@login_required(login_url='/mylogin/login/')
def index(request):

    btc_le = Bitcoin.objects.last()
    eth_le = Etherium.objects.last()

    btc_data = CalcClass().views_data(btc_le)
    eth_data = CalcClass().views_data(eth_le)

    context = {
               'btc_data': btc_data,
               'eth_data': eth_data,
              }

    return render(request, 'crypto/index.html', context)

@login_required(login_url='/mylogin/login/')
def btc(request):

    table = "bitcoin"
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            tf = form.cleaned_data['time_frame']
            script, div = GraphClass(table).graph_data(tf)
            context = {"script": script,
                       "div": div,
                       "form": form,
                       'coin': 'Bitcoin'}

            return render(request, 'crypto/btc.html', context)

    else:
        form = TimeForm()
        script, div = GraphClass(table).graph_data()
        context = {"script": script,
                   "div": div,
                   "form": form}

        return render(request, 'crypto/btc.html', context)

@login_required(login_url='/mylogin/login')
def eth(request):

    table = 'etherium'
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            tf = form.cleaned_data['time_frame']
            script, div = GraphClass(table).graph_data(tf)
            context = {"script": script,
                       "div": div,
                       "form": form,
                       'coin': 'Bitcoin'}

            return render(request, 'crypto/btc.html', context)

    else:
        form = TimeForm()
        script, div = GraphClass(table).graph_data()
        context = {'script': script,
                   'div': div,
                   'form': form,
                   'coin': 'Etherium'}

        return render(request, 'crypto/btc.html', context)

