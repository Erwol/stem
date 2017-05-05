from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from .views import custom_login

urlpatterns = [
    url(r'login/$', custom_login, name='login'),
    url(r'logout/$', auth_views.logout, name='logout'),
]