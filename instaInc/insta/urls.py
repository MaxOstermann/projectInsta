from django.conf.urls import url

from . import views

app_name = 'insta'
urlpatterns = [
    url(r'^$', views.reg, name='reg'),
    url(r'^auth/', views.login, name='login'),
    url(r'^lout/', views.lout, name='lout'),
    url(r'^exit/', views.log_out, name='exit'),
    url(r'^uspeh/', views.uspeh, name='ura'),
]