from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
import datetime
from django.utils import timezone
from django.urls import reverse
from image.models import Images
from like.models import Likes
from .serializers import *


def reg(request):
    """
    регистрация
    """
    form = OrderForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('insta:login'))

    return render(request, 'insta/reg.html', {"form": form})


def dele(request, idph):
    if (
            request.session.get('member_id', None) and
            Images.objects.get(pk=int(idph)).created_by.id == request.session['member_id']
       ):
        m = Images.objects.get(pk=int(idph))    
        m.delete()
    return HttpResponseRedirect(reverse('insta:home'))


def profile(request):
    if request.session.get('member_id', None):
        user = InstaUser.objects.get(pk=request.session['member_id'])
        return HttpResponseRedirect(reverse('insta:profile_page', kwargs={'idph': user.id}))
    else:
        return HttpResponseRedirect(reverse('insta:login'))


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


def home(request):
    imgs = Images.objects.order_by('created_at')[:5]
    context = {
        'images': imgs,
        }
    return render(request, 'insta/home.html', context)


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
