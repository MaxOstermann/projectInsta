from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *


def reg(request):
    form = OrderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect('uspeh')

    return render(request, 'insta/reg.html', {"form": form})


def addphoto(request):
    if request.session.get('member_id', None):
        m = InstaUser.objects.get(pk=request.session['member_id'])
        form = PhotoForm(request.POST or None, request.FILES or None, initial={
                             "created_by": m.id
                         })
        form.fields['created_by'].widget = forms.HiddenInput()
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponseRedirect('uspeh')

        return render(request, 'insta/addphoto.html', {"form": form, "user": m.nickname_user})
    else:
        return HttpResponse("Чтобы выложить фото, зайдите на сайт")


def profile(request):
    m = InstaUser.objects.get(pk=request.session['member_id'])
    context = {
        'id' : m.id,
        'nickname_user': m.nickname_user,
        'email_user': m.email_user,
        'image_id' : m.image_id.url
    }
    return render(request, 'insta/profile.html', context)


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
