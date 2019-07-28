from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import datetime
from django.utils import timezone
from django.urls import reverse
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def comments_list(request):
    """метод для добавления или публикации комментария"""
    if request.method == 'GET':
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = InstaUser.objects.get(pk=request.session['member_id'])
        serializer = CommentsSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=user,date=timezone.now() - datetime.timedelta(days=1))
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
    """регистрация"""
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

        return render(request, 'insta/addphoto.html',  {
            "form": form,
            "user": m.nickname_user
            })
    else:
        return HttpResponse("Чтобы выложить фото, зайдите на сайт")


def profile(request):
    if request.session.get('member_id', None):
        user = InstaUser.objects.get(pk=request.session['member_id'])
        return HttpResponseRedirect(reverse('insta:profile_page', kwargs={'idph': user.id}))


def makelike(request, idph):
    if request.session.get('member_id', None):
        image = Images.objects.get(pk=int(idph))
        user = InstaUser.objects.get(pk=request.session['member_id'])
        if Likes.objects.filter(
            picture=image,
            sender_id=user
            ).exists():
            like = Likes.objects.get(
                picture=image,
                sender_id=user
                )
            like.delete()
        else:
            like = Likes(
                picture=image,
                created=timezone.now() - datetime.timedelta(days=1),
                sender_id=user
                )
            like.save()
    return HttpResponseRedirect(reverse('insta:photo', kwargs={'idph': idph}))


def make_follow(request, id_user_to_follow):
    if request.session.get('member_id', None):
        user_to_follow = InstaUser.objects.get(pk=int(id_user_to_follow))
        follower = InstaUser.objects.get(pk=request.session['member_id'])
        if Follows.objects.filter(
            man=follower,
            follow_to=user_to_follow
            ).exists():
            follow = Follows.objects.get(
                man=follower,
                follow_to=user_to_follow
                )
            follow.delete()
        else:
            real_time = timezone.now() - datetime.timedelta(days=1)
            follow = Follows(
                man=follower,
                created=real_time,
                follow_to=user_to_follow
                )
            follow.save()
    return HttpResponseRedirect(reverse(
        'insta:profile_page',
        kwargs={'idph': id_user_to_follow}
        ))


def profile_page(request, idph):
    if request.session.get('member_id', None):
        user = InstaUser.objects.get(pk=int(idph))
        activ_user = InstaUser.objects.get(pk=request.session['member_id'])
        if Follows.objects.filter(man=activ_user, follow_to=user).exists():
            text_button = "Отписаться"
        else:
            text_button = "Подписаться"
        if user == activ_user:
            text_button = "Так это же я сам!"
        man_num = len(Follows.objects.filter(man=user))
        follow_to_num = len(Follows.objects.filter(follow_to=user))
        context = {
            'id': user.id,
            'nickname_user': user.nickname_user,
            'email_user': user.email_user,
            'image_id': user.image_id.url,
            'text_button': text_button,
            'man_num': man_num,
            'follow_to_num': follow_to_num,
            'images': Images.objects.filter(created_by=user)[:5]
            }
        return render(request, 'insta/profile_page.html', context)


def photo(request, idph):
    if request.session.get('member_id', None):
        photo_owner_user = Images.objects.get(pk=int(idph))
        activ_user = InstaUser.objects.get(pk=request.session['member_id'])
        if Likes.objects.filter(
                picture=photo_owner_user,
                sender_id=activ_user
        ).exists():
            text_button = "Мне больше не нравится"
        else:
            text_button = "Мне нравится"
        like_len = len(Likes.objects.filter(picture=photo_owner_user))
        form = CommentForm(request.POST or None, request.FILES or None, initial={
            "publication_id": photo_owner_user.id,
            "date" : timezone.now() - datetime.timedelta(days=1),
            "sender_id" : activ_user.id,
            })
        form.fields['sender_id'].widget = forms.HiddenInput()
        form.fields['publication_id'].widget = forms.HiddenInput()
        form.fields['date'].widget = forms.HiddenInput()
        if request.method == "POST" and form.is_valid():
            form.save()
        create = InstaUser.objects.get(pk=photo_owner_user.created_by.id).nickname_user
        send_user = InstaUser.objects.get(pk=photo_owner_user.created_by.id).id
        context = {
            'id' : photo_owner_user.id,
            'created_by': create,
            'created_id': send_user,
            'created_at': photo_owner_user.created_at,
            'image_id' : photo_owner_user.image_id.url,
            'form' : form,
            'l_num': like_len,
            'text_button': text_button,
            }
        try:
            com = Comments.objects.filter(publication_id=photo_owner_user.id)#[:5]
            context['comments'] = com
        except Comments.DoesNotExist:
            pass

        return render(request, 'insta/photo.html', context)
    else:
        return HttpResponse("Чтобы посмотреть фото, зайдите на сайт")


def home(request):
    imgs = Images.objects.order_by('created_at')[:5]
    context = {
        'images': imgs,
        }
    return render(request, 'insta/home.html', context)


def uspeh(request):
    return render(request, 'insta/uspeh.html')


def login(request):
    if request.method == "POST":
        try:
            login_user = InstaUser.objects.get(nickname_user=request.POST['username'])
            if login_user.password == request.POST['password']:
                request.session['member_id'] = login_user.id
                return HttpResponseRedirect( reverse('insta:home'))
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
