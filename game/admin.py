from django.contrib import admin
from .models import Question, TestOption, TextQuestionAnswer, Cheat, Story, UserAnswer
# Register your models here.

class CheatInline(admin.StackedInline):
    model = Cheat
    min_num = 0
    max_num = 5
    classes = ('collapse',)

class TestOptionInline(admin.StackedInline):
    model = TestOption
    max_num = 5
    classes = ('collapse',)
    # Includes the answer

class TextQuestionAnswerInline(admin.StackedInline):
    model = TextQuestionAnswer
    max_num = 1
    classes = ('collapse',)

class QuestionAdmin(admin.ModelAdmin):
    inlines = (CheatInline, TestOptionInline, TextQuestionAnswerInline, )




admin.site.register(UserAnswer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Story)