from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import login
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView

from game.models import *

class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = "games/game-list.html"
    login_url = 'login'

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)

class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['story']
    template_name = "games/game-create.html"
    login_url = 'login'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GameCreateView, self).form_valid(form)

class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = "games/game-delete.html"
    success_url = reverse_lazy('home')

class GameQuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "question/question-list.html"
    login_url = 'login'

    def get_queryset(self):
        return Question.objects.filter(story__in=
           Game.objects.filter(pk__in=self.kwargs['pk']).values('story'))


