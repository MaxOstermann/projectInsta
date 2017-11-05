from django.conf.urls import url

from . import views

app_name = 'insta'
urlpatterns = [
    url(r'^$', views.reg, name='reg'),
    url(r'^uspeh/', views.uspeh, name='ura'),
]