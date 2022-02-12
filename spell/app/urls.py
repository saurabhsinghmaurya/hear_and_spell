from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login', views.login, name='login'),
    re_path(r'^register', views.register, name='reg'),
    re_path(r'^start', views.start, name='start'),
    re_path(r'^logout', views.logout, name='logout'),
    re_path(r'^stop', views.stop, name='stop'),
    re_path(r'^check', views.check, name='check'),
    re_path(r'^word', views.word_info, name='word_info'),
    re_path(r'^resume', views.resume_test, name='resume_test'),
]
