from django.conf.urls import  url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'like'
urlpatterns = [
    url(r'^makelike/(?P<idph>.+)/$', views.makelike, name='makelike'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
