from question.models import *
from django import forms


class AnswerForm(forms.ModelForm):
    class Meta:
        model = TextQuestionAnswer