from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .forms import *
import datetime
from django.utils import timezone


def reg(request):
    form = OrderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect('uspeh')

    return render(request, 'insta/reg.html', {"form": form})


def uspeh(request):
    return render(request, 'insta/uspeh.html')


def login(request):
    if request.method == "POST":
        try:
            m = InstaUser.objects.get(nickname_user=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['member_id'] = m.id
                return HttpResponse("Вы авторизованы.")
            else:
                return HttpResponse("Неправильный пароль.")
        except InstaUser.DoesNotExist:
            return HttpResponse("Ваши логин и пароль не соответствуют.")

    return render(request, 'insta/auth.html')


def lout(request):
    return render(request, 'insta/lout.html')


def log_out(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass

    return HttpResponse("Вы вышли.")
