from django.conf.urls import  url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'image'
urlpatterns = [
    url(r'^addphoto/', views.addphoto, name='addphoto'),
    url(r'^dele/(?P<idph>.+)/$', views.dele, name='dele'),
    url(r'^photo/(?P<idph>.+)/$', views.photo, name='photo'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
