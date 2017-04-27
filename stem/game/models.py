from django.db import models
from user.models import Base, User
from question.models import Story, Question
from django.utils.translation import ugettext_lazy as _
# Create your models here.





class Game(Base):
    """ Partida de un usuario particular """
    user = models.ForeignKey(User, help_text=_("Usuario que juega la partida"))
    story = models.ForeignKey(Story, help_text=_("Historia seleccionada por el jugador"))
    is_finished = models.BooleanField(_("¿Ha terminado el juego?"), default=False)
    is_started = models.BooleanField(_("¿Ha comenzado el juego?"), default=False)


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


class GameQuestions(Base):
    """ Original PartidaPregunta | Preguntas asociadas a una partida """
    game = models.ForeignKey(Game)
    question = models.ForeignKey(Question)

    class Meta:
        verbose_name = _("Preguntas de la partida")