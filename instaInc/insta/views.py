from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .forms import *
import datetime
from django.utils import timezone


def reg(request):
    form = OrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    return render(request, 'insta/reg.html', {"form": form})

def uspeh(request):
    return render(request, 'insta/uspeh.html')