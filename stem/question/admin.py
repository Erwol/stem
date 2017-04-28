from django.contrib import admin
from .models import Question, TestOption, TextQuestionAnswer, TextQuestion, Cheat
# Register your models here.

class CheatInline(admin.StackedInline):
    model = Cheat
    min_num = 0
    max_num = 5
    classes = ('collapse',)

class TestOptionInline(admin.StackedInline):
    model = TestOption
    # Includes the answer



class QuestionAdmin(admin.ModelAdmin):
    inlines = (CheatInline, TestOptionInline, )

    # TODO When the admin selects one or another question type, a different inline appears https://docs.djangoproject.com/en/1.10/ref/contrib/admin/javascript/




admin.site.register(Question, QuestionAdmin)