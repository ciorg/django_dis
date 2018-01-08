from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TimeForm

from .visualizer import Bitcoin

@login_required(login_url='/mylogin/login/')
def index(request):
    context = {}
    return render(request, 'crypto/index.html', context)

@login_required(login_url='/mylogin/login/')
def btc(request):

    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            tf = form.cleaned_data['time_frame']
            script, div = Bitcoin().graph_data(tf)
            context = {"script": script,
                       "div": div,
                       "form": form}

            return render(request, 'crypto/btc.html', context)

    else:
        form = TimeForm()
        script, div = Bitcoin().graph_data()
        context = {"script": script,
                   "div": div,
                   "form": form}

        return render(request, 'crypto/btc.html', context)
