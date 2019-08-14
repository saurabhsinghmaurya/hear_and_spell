from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='reg'),
    url(r'^start', views.start, name='start'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^stop', views.stop, name='stop'),
    url(r'^check', views.check, name='check'),

]
