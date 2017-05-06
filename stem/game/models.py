from django.db import models
from user.models import User, Base
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator
# Create your models here.


class Story(Base):
    """ Historia """
    name = models.CharField(_("Nombre de la historia"), max_length=128, blank=False)
    context = models.TextField(_("Contexto en el que se desarrolla el juego"), help_text=_("Ejemplo: Florinda y Torcuato están preparándose para una aventura, ¿te animas a ayudarlos?"))
    min_age = models.IntegerField(_("Edad mínima recomendada"), default=10)
    max_age = models.IntegerField(_("Edad máxima recomendada"), default=13)

    #
    questions_number = models.IntegerField(default=0, editable=False, help_text=_("Número autogenerado de preguntas de una historia"))

    cover = models.ImageField(_("Imagen de portada de la historia (500 x 500)"), blank=True, upload_to="covers")


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

    def get_questions_number(self):
        """ Número total y autogenerado de preguntas """
        return self.questions_number

    def __str__(self):
        return self.name


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


class Question(Base):
    """ Preguntas de la historia """
    story = models.ForeignKey(Story, help_text=_("Historia a la que pertenece la pregunta"), blank=False, null=False, )
    order = models.PositiveIntegerField(_("Orden de la pregunta en el juego"), validators=[MinValueValidator(1)])

    QUESTION_TYPES = (
        ('TEXTO', _('Texto')),
        ('CUESTIONARIO', _('Cuestionario')),
        ('VINETA', _('Viñeta')),
    )

    type = models.CharField(_("Tipo de pregunta"), choices=QUESTION_TYPES, default='TEXTO', max_length=128, help_text=_("Texto, cuestionario, etc"))
    image = models.ImageField(_("Imagen que se mostrará en la cabecera de la pregunta"), null=True, blank=True)
    text = models.TextField(_("Enunciado de la pregunta."))

    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")
        unique_together = ("story", "order", )

    def get_question_type(self):
        return self.question_type

    def get_image(self):
        return self.image

    def get_order(self):
        return self.order

    def __str__(self):
        return ("%d@%s") % (self.order, self.story.name)

@receiver(post_save, sender=Question)
def increase_story_questions_number(sender, instance=None, created=False, **kwargs):
    if created:
        # Obtiene la historia de la instancia y aumenta el número de preguntas
        story = Story.objects.get(id=instance.story.id)
        story.questions_number += 1
        story.save()

@receiver(pre_delete, sender=Question)
def decrease_story_questions_number(sender, instance=None, created=False, **kwargs):
    # Obtiene la historia de la instancia y aumenta el número de preguntas
    story = Story.objects.get(id=instance.story.id)
    story.questions_number -= 1
    story.save()


class Cheat(Base):
    """ Pistas de las preguntas """
    question = models.ForeignKey(Question, blank=False, null=False)
    order = models.IntegerField(_("Órden de las pistas, del 1 a n"), default=1, validators=[MinValueValidator(1)], help_text=_("No repitas el orden de las pistas"))
    text = models.TextField(_("Texto de la pista"))
    class Meta:
        verbose_name = _("Pista")
        verbose_name_plural = _("Pistas")
        unique_together = ('question', 'order')

    def get_question(self):
        return self.question

    def get_order(self):
        return self.order


class TextQuestionAnswer(Base):
    """ El enunciado está en la pregunta; la respuesta aquí """
    question = models.ForeignKey(Question, blank=False, null=False)
    answer = models.TextField(_("Respuesta a la pregunta"))
    class Meta:
        verbose_name = _("Respuesta a pregunta de tipo texto")
        verbose_name_plural = _("Respuestas a preguntas de tipo texto")

    def get_question(self):
        return self.question

    def get_text(self):
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
        return self.text

    def get_is_active(self):
        return self.is_active

    def get_text(self):
        return self.text





