from django.conf.urls import  url
from django.conf import settings
from django.conf.urls.static import static

from insta import views

app_name = 'insta'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^reg/', views.reg, name='reg'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^profile_page/(?P<idph>.+)/$', views.profile_page, name='profile_page'),
    url(r'^auth/', views.login, name='login'),
    url(r'^lout/', views.lout, name='lout'),
    url(r'^exit/', views.log_out, name='exit'),
    url(r'^uspeh/', views.uspeh, name='ura'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
