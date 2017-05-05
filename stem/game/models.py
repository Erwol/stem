# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from user.models import Base, User
from question.models import Story, Question
from django.utils.translation import ugettext_lazy as _
# Create your models here.





class Game(Base):
    """ Partida de un usuario e historia particular """
    user = models.ForeignKey(User, help_text=_("Usuario que juega la partida"))
    story = models.ForeignKey(Story, help_text=_("Historia seleccionada por el jugador"))
    is_finished = models.BooleanField(_("¿Ha terminado el juego?"), default=False)
    actual_question = models.IntegerField(_("Pregunta actual, desde 1 hasta num pregs"), editable=False, default=0)

    class Meta:
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"


    def game_over(self):
        """ Determina si se han recorrido todas las preguntas del juego """
        return self.is_finished and self.is_started

    def get_user(self):
        return self.user

    def get_story(self):
        return self.story

    def get_is_finished(self):
        return self.is_finished

    def get_is_started(self):
        return self.is_started
