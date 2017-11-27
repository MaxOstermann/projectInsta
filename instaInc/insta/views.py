from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def comments_list(request):

    if request.method == 'GET':
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        us = InstaUser.objects.get(pk=request.session['member_id'])
        serializer = CommentsSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=us,date=timezone.now() - datetime.timedelta(days=1))
            return Response('OK', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def profile_list(request):

    if request.method == 'GET':
        users = InstaUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('OK', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_api(request):
    if request.method == "POST":
        try:
            m = InstaUser.objects.get(nickname_user=request.data['username'])
            if m.password == request.data['password']:
                request.session['member_id'] = m.id
                return Response("Вы авторизованы.")
            else:
                return Response("Неправильный пароль.")
        except InstaUser.DoesNotExist:
            return Response("Ваши логин и пароль не соответствуют.")


@api_view(['GET'])
def lout_api(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass

    return Response("Вы вышли.")


def reg(request):
    form = OrderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('insta:login'))

    return render(request, 'insta/reg.html', {"form": form})


def dele(request, idph):
    if request.session.get('member_id', None) and Images.objects.get(pk=int(idph)).created_by.id == request.session['member_id']:
        m = Images.objects.get(pk=int(idph))    
        m.delete()
    return HttpResponseRedirect(reverse('insta:home'))

def addphoto(request):
    if request.session.get('member_id', None):
        m = InstaUser.objects.get(pk=request.session['member_id'])
        form = PhotoForm(request.POST or None, request.FILES or None, initial={
                             "created_by": m.id
                         })
        form.fields['created_by'].widget = forms.HiddenInput()
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('insta:ura'))

        return render(request, 'insta/addphoto.html', {"form": form, "user": m.nickname_user})
    else:
        return HttpResponse("Чтобы выложить фото, зайдите на сайт")


def profile(request):
    if request.session.get('member_id', None):
        m = InstaUser.objects.get(pk=request.session['member_id'])
        context = {
            'id' : m.id,
            'nickname_user': m.nickname_user,
            'email_user': m.email_user,
            'image_id' : m.image_id.url
        }
        return render(request, 'insta/profile.html', context)
    else:
        return HttpResponse("Чтобы посмотреть свою страницу, зайдите на сайт")


def makelike(request, idph):
    if request.session.get('member_id', None):
        m = Images.objects.get(pk=int(idph))
        us = InstaUser.objects.get(pk=request.session['member_id'])
        if Likes.objects.filter(
            picture=m,
            sender_id=us
        ).exists():
            lokas = Likes.objects.filter(
                picture=m,
                sender_id=us
            )[0]
            lokas.delete()
        else:
            like = Likes(picture=m, created=timezone.now() - datetime.timedelta(days=1),
                         sender_id=us)
            like.save()
    return HttpResponseRedirect(reverse('insta:photo', kwargs={'idph': idph}))


def photo(request, idph):
    if request.session.get('member_id', None):
        m = Images.objects.get(pk=int(idph))
        us = InstaUser.objects.get(pk=request.session['member_id'])
        if Likes.objects.filter(
                picture=m,
                sender_id=us
        ).exists():
            text_button = "Мне больше не нравится"
        else:
            text_button = "Мне нравится"
        liik = len(Likes.objects.filter(picture=m))
        form = CommentForm(request.POST or None, request.FILES or None, initial={
                             "publication_id": m.id,
                             "date" : timezone.now() - datetime.timedelta(days=1),
                             "sender_id" : us.id,
                         })
        form.fields['sender_id'].widget = forms.HiddenInput()
        form.fields['publication_id'].widget = forms.HiddenInput()
        form.fields['date'].widget = forms.HiddenInput()
        if request.method == "POST" and form.is_valid():
            form.save()
        create = InstaUser.objects.get(pk=m.created_by.id).nickname_user
        context = {
            'id' : m.id,
            'created_by': create,
            'created_at': m.created_at,
            'image_id' : m.image_id.url,
            'form' : form,
            'l_num': liik,
            'text_button': text_button,
        }
        try:
            com = Comments.objects.filter(publication_id=m.id)#[:5]
            context['comments'] = com
        except Comments.DoesNotExist:
            pass

        return render(request, 'insta/photo.html', context)
    else:
        return HttpResponse("Чтобы посмотреть фото, зайдите на сайт")


def home(request):
    context = {
        'images': Images.objects.order_by('created_at')[:5]
    }
    return render(request, 'insta/home.html', context)


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
