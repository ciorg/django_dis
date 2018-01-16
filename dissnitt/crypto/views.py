from collections import namedtuple
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calcs import CalcClass
from .forms import TimeForm
from .visualizer import GraphClass
from .models import Bitcoin, Etherium, EtheriumBTC, Litecoin, LitecoinBTC, RippleBTC, MoneroBTC, BitcashBTC


@login_required(login_url='/mylogin/login/')
def index(request):

    btc_le = Bitcoin.objects.last()

    ethbtc_data = CalcClass().views_data(EtheriumBTC.objects.last())
    ltcbtc_data = CalcClass().views_data(LitecoinBTC.objects.last())
    xrpbtc_data = CalcClass().views_data(RippleBTC.objects.last())
    xmrbtc_data = CalcClass().views_data(MoneroBTC.objects.last())
    bchbtc_data = CalcClass().views_data(BitcashBTC.objects.last())

    btc_price = float(btc_le.gdax_price)
    ethbtc_usd = btc_price * ethbtc_data[0]
    ltcbtc_usd = btc_price * ltcbtc_data[0]
    xrpbtc_usd = btc_price * xrpbtc_data[0]
    xmrbtc_usd = btc_price * xmrbtc_data[0]
    bchbtc_usd = btc_price * bchbtc_data[0]

    context = {
               'btc': CalcClass().views_data(btc_le),
               'eth': CalcClass().views_data(Etherium.objects.last()),
               'ltc': CalcClass().views_data(Litecoin.objects.last()),
               'ethbtc': ethbtc_data,
               'ethbtc_usd': ethbtc_usd,
               'ethbtc_start_usd': ethbtc_data[3] * btc_price,
               'ethbtc_end_usd': ethbtc_data[4] * btc_price,
               'ltcbtc': ltcbtc_data,
               'ltcbtc_usd': ltcbtc_usd,
               'ltcbtc_start_usd': ltcbtc_data[3] * btc_price,
               'ltcbtc_end_usd': ltcbtc_data[4] * btc_price,
               'xrpbtc': xrpbtc_data,
               'xrpbtc_usd': xrpbtc_usd,
               'xrpbtc_start_usd': xrpbtc_data[3] * btc_price,
               'xrpbtc_end_usd': xrpbtc_data[4] * btc_price,
               'xmrbtc': xmrbtc_data,
               'xmrbtc_usd': xmrbtc_usd,
               'xmrbtc_start_usd': xmrbtc_data[3] * btc_price,
               'xmrbtc_end_usd': xmrbtc_data[4] * btc_price,
               'bchbtc': bchbtc_data,
               'bchbtc_usd': bchbtc_usd,
               'bchbtc_start_usd': bchbtc_data[3] * btc_price,
               'bchbtc_end_usd': bchbtc_data[4] * btc_price,
              }

    return render(request, 'crypto/index.html', context)


@login_required(login_url='/mylogin/login/')
def pdatag(request, table):

    cdict = {'bitcoin': 'BTC/USD',
             'etherium': 'ETH/USD',
             'etheriumbtc': 'ETH/BTC',
             'litecoin': 'LTC/USD',
             'litecoinbtc': 'LTC/BTC',
             'monerobtc': 'XMR/BTC',
             'ripplebtc': 'XRP/BTC',
             'bitcashbtc': 'BCH/BTC'}

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
