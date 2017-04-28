from django.contrib import admin
from .models import Question, TestQuestion, TestOption, TextQuestionAnswer, TextQuestion, Cheat
# Register your models here.

class CheatInline(admin.StackedInline):
    model = Cheat



class QuestionAdmin(admin.ModelAdmin):
    inlines = (CheatInline, )



admin.site.register(Question, QuestionAdmin)
admin.site.register(TestQuestion)