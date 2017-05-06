from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from .views import custom_login

app_name = 'user'

urlpatterns = [
    #url(r'login/$', custom_login, name='login'),
    url(r'^$', custom_login, name='index'), # TODO Susutituir home por web real con información del proyecto
    url(r'logout/$', auth_views.logout, name='logout'), # Elimina por defecto todas las keys de sesión
]