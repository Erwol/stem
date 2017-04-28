from django.contrib import admin
from .models import Question, TestOption, TextQuestion, Cheat, Story
# Register your models here.

class CheatInline(admin.StackedInline):
    model = Cheat
    min_num = 0
    max_num = 5
    classes = ('collapse',)

class TestOptionInline(admin.StackedInline):
    model = TestOption
    max_num = 5
    # Includes the answer

class TextQuestionInline(admin.StackedInline):
    model = TextQuestion
    max_num = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = (CheatInline, TestOptionInline, TextQuestionInline, )





admin.site.register(Question, QuestionAdmin)
admin.site.register(Story)