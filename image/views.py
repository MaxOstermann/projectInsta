from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from image.forms import PhotoForm
from comment.forms import CommentForm
from django import forms
import datetime
from django.utils import timezone
from django.urls import reverse
from insta.models import InstaUser
from comment.models import Comments
from image.models import Images
from like.models import Likes


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
            return HttpResponseRedirect(reverse('image:photo', kwargs={'idph': form.instance.id}))

        return render(request, 'image/addphoto.html',  {
            "form": form,
            "user": m.nickname_user
            })
    else:
        return HttpResponse("Чтобы выложить фото, зайдите на сайт")


def photo(request, idph):
    '''

    :param request:
    :param idph:
    :return:
    '''
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

        return render(request, 'image/photo.html', context)
    else:
        return HttpResponse("Чтобы посмотреть фото, зайдите на сайт")

