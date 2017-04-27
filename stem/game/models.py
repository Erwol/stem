from django.db import models
from user.models import Base, User
from django.utils.translation import ugettext_lazy as _
# Create your models here.




class Game(Base):
    user = models.ForeignKey(User)
    is_finished = models.BooleanField(_("¿Ha terminado el juego?"), default=False)
    is_started = models.BooleanField(_("¿Ha comenzado el juego?"), default=False)


    def game_over(self):
        """ Determina si se han recorrido todas las preguntas del juego """
        return self.is_finished and self.is_started