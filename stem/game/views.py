from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import login
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from game.models import *

class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = "games/game-list.html"
    # login_url = 'user:login'

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)

class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    fields = ['story']
    template_name = "games/game-create.html"
    login_url = 'user:login'
    success_url = reverse_lazy('game:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GameCreateView, self).form_valid(form)

class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    template_name = "games/game-delete.html"
    success_url = reverse_lazy('game:home')

class GameQuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "question/question-list.html"
    login_url = 'login'

    def get_queryset(self):
        return Question.objects.filter(story__in=
           Game.objects.filter(pk__in=self.kwargs['pk']).values('story'))



# Inicializa y recupera previas partidas del juego
def play_game(request, game_id):
    # Comprobamos método de acceso a la función
    if(request.method == "POST"):
        game_id = request.POST.get("game_id", )
        # TODO Comprobar si la partida existe realmente y está asociada a este usuario
        game = get_object_or_404(Game, pk=game_id)
        story = game.story

        if(story.questions_number == 0):
            return HttpResponseRedirect(reverse('game:home', )) # TODO Devolver errores


        request.session["game_id"] = game.id
        request.session["story_id"] = story.id
        request.session["actual_question"] = game.actual_question # Pregunta actual, inicializada a 0

        return redirect('game:game-controller')
        # return redirect('view', var1=value1)


    else:
        return HttpResponseRedirect(reverse('game:home',))



def game_controller(request):
    """ Controla la ejecución secuencial de las preguntas """
    # El juego termina cuando la pregunta actual es igual al número total de preguntas
    actual_question = request.session["actual_question"]
    story_id = request.session["story_id"]

    story = get_object_or_404(Story, pk=story_id)
    # Accedemos a la pregunta que le toca al usuario
    question = Question.objects.filter(story=story).order_by('order')[actual_question]

    # Si la pregunta es de tipo test, pasamos el cuestionario
    answers = list()
    if question.type == "CUESTIONARIO":
        answers = TestOption.objects.filter(question=question)

    # Y también enviamos el número de pistas que tiene la pregunta
    cheat_number = Cheat.objects.filter(question=question).count()
    return render(request, 'question/question.html', {
        'question': question,
        'answers': answers,
        'cheat_number': cheat_number,
        'progress': 10, # TODO Calcular el progreso y mostrarlo en un porcentaje?
    })


# Control del guardado de respuestas
def save_response(request):
    """ Sólo se guarda la respuesta y se avanza en la pregunta si el usuario la ha respondido """
    actual_question = request.session["actual_question"]
    story_id = request.session["story_id"]
    game_id = request.session["game_id"]
    story = get_object_or_404(Story, pk=story_id)
    game = get_object_or_404(Game, pk=game_id)
    actual_question += 1
    request.session["actual_question"] = actual_question

    # Guardamos el progreso en la base de datos por si el usuario quiere continuar más tarde
    game.actual_question = actual_question
    game.save()

    if actual_question >= story.get_questions_number():
        # TODO Mandar al usuario a una pantalla en la que vea los resultados
        game.is_finished = True # Guardando este valor, esta partida será guardada como completada, aunque en un futuro se alteren las preguntas del test
        game.save()
        return HttpResponseRedirect(reverse('game:home', ))

    return HttpResponseRedirect(reverse('game:game-controller', ))


def get_cheat(request, question_id, cheat_count):
    if(request.method == "GET"):
        question = get_object_or_404(Question, pk=question_id)
        if Cheat.objects.filter(question=question)[int(cheat_count)]:
            cheat = Cheat.objects.filter(question=question)[int(cheat_count)]
            return HttpResponse(cheat.text, status=200)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponseNotAllowed()