from django.conf.urls import url, include
from game.views import RankingListView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import *
# Necesario para las llamadas via POST
app_name = 'game'

urlpatterns = [
    url(r'^dashboard$', GameListView.as_view(), name='home'),  # User home
    url(r'^delete/(?P<pk>\d+)$', GameDeleteView.as_view(), name='game-delete'),
    
    url(r'^create/$', GameCreateView.as_view(), name='game-create'),
    url(r'^(?P<pk>\d+)$', GameQuestionListView.as_view(), name='question-list'),
    url(r'^ranking/$', RankingListView.as_view(), name='ranking-list'),

    url(r'^play-game/(?P<game_id>[0-9]+)/$', play_game, name='play-game'),
    url(r'^game-controller/$', game_controller, name='game-controller'),
    url(r'^save-response/$', save_response, name='save-response'),

    # Devuelve el texto de la pista
    url(r'^question-cheat/(?P<question_id>[0-9]+)/(?P<cheat_count>[0-9]+)/$', get_cheat, name='get-cheat'),

    # Devuelve la media de puntos obtenidos en esta partida
    url(r'^game-points/(?P<game_id>[0-9]+)/$', get_game_points, name='get-game-points'),


]