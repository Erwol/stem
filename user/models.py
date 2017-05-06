# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import date

class Base(models.Model):
    creation_date = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    modification_date = models.DateTimeField(_("Fecha de modificación"), auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    is_student = models.BooleanField(_("Es estudiante"), default=True, help_text=_("Opción mostrada solo en la administración"))
    date_of_birth = models.DateField(_("Fecha de nacimiento"), default=timezone.now)
    email = models.EmailField(_("Correo electrónico"), max_length=254, unique=True, blank=False)

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    def get_age(self):
        """ Edad del usuario expresada en años """
        return date.today().year - self.date_of_birth.year

