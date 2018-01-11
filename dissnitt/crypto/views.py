from collections import namedtuple
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .calcs import CalcClass
from .forms import TimeForm
from .visualizer import GraphClass
from .models import Bitcoin

@login_required(login_url='/mylogin/login/')
def index(request):

    last_entry = Bitcoin.objects.last()
    profit = CalcClass().views_data(last_entry)

    context = {
               'profit': profit[0],
               'dir': profit[1],
               'pp': profit[2],
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
                       "form": form}

            return render(request, 'crypto/btc.html', context)

    else:
        form = TimeForm()
        script, div = GraphClass(table).graph_data()
        context = {"script": script,
                   "div": div,
                   "form": form}

        return render(request, 'crypto/btc.html', context)
