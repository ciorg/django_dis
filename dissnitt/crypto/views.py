from collections import namedtuple
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calcs import CalcClass
from .forms import TimeForm
from .visualizer import GraphClass
from .models import Bitcoin, Etherium, EtheriumBTC


@login_required(login_url='/mylogin/login/')
def index(request):

    btc_le = Bitcoin.objects.last()
    eth_le = Etherium.objects.last()
    ethbtc_le = EtheriumBTC.objects.last()

    btc_data = CalcClass().views_data(btc_le)
    eth_data = CalcClass().views_data(eth_le)
    ethbtc_data = CalcClass().views_data(ethbtc_le)

    context = {
               'btc_data': btc_data,
               'eth_data': eth_data,
               'ethbtc_data': ethbtc_data
              }

    return render(request, 'crypto/index.html', context)


@login_required(login_url='/mylogin/login/')
def pdatag(request, table):

    cdict = {'bitcoin': 'BTC/USD',
             'etherium': 'ETH/USD',
             'etheriumbtc': 'ETH/BTC'}

    cur = cdict.get(table)

    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            tf = form.cleaned_data['time_frame']
            script, div = GraphClass(table).graph_data(tf)
            context = {"script": script,
                       "div": div,
                       "form": form,
                       'cur': cur}

            return render(request, 'crypto/btc.html', context)

    else:
        form = TimeForm()
        script, div = GraphClass(table).graph_data()
        context = {"script": script,
                   "div": div,
                   "form": form,
                   "cur": cur}

        return render(request, 'crypto/btc.html', context)
