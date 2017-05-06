from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import GameCreateView, GameDeleteView, GameListView, GameQuestionListView, play_game, game_controller

# Necesario para las llamadas via POST
app_name = 'game'

urlpatterns = [
    url(r'^create/$', GameCreateView.as_view(), name='game-create'),
    url(r'^(?P<pk>\d+)$', GameQuestionListView.as_view(), name='question-list'),

    url(r'^play-game/(?P<game_id>[0-9]+)/$', play_game, name='play-game'),
    url(r'^game-controller/$', game_controller, name='game-controller'),

    url(r'^$', GameListView.as_view(), name='index'), # User home
    url(r'^delete/(?P<pk>\d+)$', GameDeleteView.as_view(), name='game-delete'),
]