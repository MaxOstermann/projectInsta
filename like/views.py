from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.utils import timezone
from django.urls import reverse
from image.models import Images
from like.models import Likes
from insta.serializers import *



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
    return HttpResponseRedirect(reverse('image:photo', kwargs={'idph': idph}))

