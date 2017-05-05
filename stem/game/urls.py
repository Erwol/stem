from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import GameCreateView, GameDeleteView, GameListView, GameQuestionListView

urlpatterns = [
    url(r'^games/create/$', GameCreateView.as_view(), name='game-create'),
    url(r'^game/(?P<pk>\d+)$', GameQuestionListView.as_view(), name='question-list'),
    url(r'^$', GameListView.as_view(), name='home'),
    url(r'^delete/(?P<pk>\d+)$', GameDeleteView.as_view(), name='game-delete'),
]