from django.db import models
from user.models import User, Base
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Story(Base):
    name = models.CharField(_("Nombre de la historia"), max_length=128, blank=False)
    context = models.TextField(_("Contexto en el que se desarrolla el juego"), help_text=_("Ejemplo: Florinda y Torcuato están preparándose para una aventura..."))
    min_age = models.IntegerField(_("Edad mínima recomendada"))