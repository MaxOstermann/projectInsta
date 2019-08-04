from django.conf.urls import  url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'insta'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^reg/', views.reg, name='reg'),
    # url(r'^comments/$', views.comments_list, name='comments_list'), #API
    url(r'^profile/', views.profile, name='profile'),
    url(r'^profile_page/(?P<idph>.+)/$', views.profile_page, name='profile_page'),
    # url(r'^profile_list_api/', views.profile_list, name='profile_list_api'), #API
    url(r'^auth/', views.login, name='login'),
    # url(r'^auth_api/', views.login_api, name='login_7api'), #API
    url(r'^lout/', views.lout, name='lout'),
    # url(r'^lout_api/', views.lout_api, name='lout_api'), #API
    url(r'^exit/', views.log_out, name='exit'),
    url(r'^uspeh/', views.uspeh, name='ura'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
