from django.db import models
from user.models import User, Base
from django.utils.translation import ugettext_lazy as _


class Story(Base):
    """ Historia """
    name = models.CharField(_("Nombre de la historia"), max_length=128, blank=False)
    context = models.TextField(_("Contexto en el que se desarrolla el juego"), help_text=_("Ejemplo: Florinda y Torcuato están preparándose para una aventura, ¿te animas a ayudarlos?"))
    min_age = models.IntegerField(_("Edad mínima recomendada"), default=10)
    max_age = models.IntegerField(_("Edad máxima recomendada"), default=13)

    #
    per_game_questions_number = models.IntegerField(_("Número de preguntas por partida"), default=5)

    cover = models.ImageField(_("Imagen de portada de la historia (500 x 500)"))

    introduction_image = models.ImageField(_("Imagen que se muestra al inicio de la partida"))
    introduction_text = models.TextField(_("Texto de introducción a la historia"), help_text=_("Es el texto que se muestra al iniciar el juego"))
    end_image = models.ImageField(_("Imagen final"))
    end_text = models.TextField(_("Texto que da fin a la historia"), help_text=_("Ejemplo: ¡Gracias a ti Torcuato lo ha logrado!"))

    class Meta:
        verbose_name = _("Historia")
        verbose_name_plural = _("Historias")

    def get_name(self):
        return self.name

    def get_min_age(self):
        return self.min_age

    def get_max_age(self):
        return self.max_age

    def get_context(self):
        return self.context

    def get_game_questions_number(self):
        """ Número de preguntas que se mostrarán al jugador al niciar una partida """
        return self.per_game_questions_number

    # TODO Añadir principio y final

class Question(Base):
    """ Preguntas de la historia """
    story = models.ForeignKey(Story, help_text=_("Historia a la que pertenece la pregunta"), blank=False, null=False, )

    TEXT = 0
    TEST = 1
    QUESTION_TYPES = (
        (TEXT, _("Texto")),
        (TEST, _("Cuestionario")),
    )

    question_type = models.CharField(_("Tipo de pregunta"), choices=QUESTION_TYPES, default=TEXT, max_length=128, help_text=_("Texto, cuestionario, etc"))
    image = models.ImageField(_("Imagen que se mostrará en la cabecera de la pregunta"), null=True)


    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")

    def get_question_type(self):
        return self.question_type

    def get_image(self):
        return self.image


class Cheat(Base):
    """ Pistas de las preguntas """
    question = models.ForeignKey(Question, blank=False, null=False)
    order = models.IntegerField(_("Órden de las pistas, del 0 a n"), default=0)
    cheat_text = models.TextField(_("Texto de la pista"))
    class Meta:
        verbose_name = _("Pista")
        verbose_name_plural = _("Pistas")

    def get_question(self):
        return self.question

    def get_order(self):
        return self.order

class TextQuestion(Base):
    """ Preguntas de tipo texto """
    question = models.ForeignKey(Question, blank=False, null=False)
    question_text = models.TextField(_("Enunciado de la pregunta."))
    answer = models.TextField(_("Respuesta a la pregunta"))
    class Meta:
        verbose_name = _("Pregunta de tipo texto")
        verbose_name_plural = _("Preguntas de tipo texto")

    def get_question(self):
        return self.question

    def get_text(self):
        return self.text

    def get_answer(self):
        return self.answer




class TestOption(Base):
    """ Opciones a responder en una pregunta de tipo test """
    question = models.ForeignKey(Question, blank=False, null=False)
    is_active = models.BooleanField(_("¿Quiere que esta opción sea visible?"), default=True)
    is_answer = models.BooleanField(_("Solución a la pregunta tipo test (puede haber varias)"), default=False)
    text = models.CharField(_("Opción de pregunta tipo test"), max_length=512)

    class Meta:
        verbose_name = _("Opción a responder en pregunta de tipo test")
        verbose_name_plural = _("Opciones a responder en pregunta de tipo test")

    def get_test(self):
        return self.test

    def get_is_active(self):
        return self.is_active

    def get_text(self):
        return self.text




