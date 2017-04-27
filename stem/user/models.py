from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Base(models.Model):
    creation_date = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)
    modification_date = models.DateTimeField(_("Fecha de modificación"), auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    is_student = models.BooleanField(_("¿Es el usuario estudiante?"), default=True)
    date_of_birth = models.DateField(_("Fecha de nacimiento"), default=timezone.now)

