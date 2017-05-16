from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import login
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from game.models import *
from django.views.decorators.http import require_http_methods
from datetime import datetime


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
@require_http_methods(["POST"])
def play_game(request, game_id):
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




@require_http_methods(["POST", "GET"])
def game_controller(request):
    """ Controla la ejecución secuencial de las preguntas """
    # El juego termina cuando la pregunta actual es igual al número total de preguntas
    actual_question = request.session["actual_question"]
    story_id = request.session["story_id"]

    story = get_object_or_404(Story, pk=story_id)
    # Accedemos a la pregunta que le toca al usuario
    question = Question.objects.filter(story=story).order_by('order')[actual_question]

    # Guardamos el id de la pregunta actual (necesario para enlazar la respuesta)
    request.session["actual_question_id"] = question.id

    # Si la pregunta es de tipo test, pasamos el cuestionario
    answers = list()
    if question.type == "CUESTIONARIO":
        answers = TestOption.objects.filter(question=question)

    # Inicializamos el penalizador de preguntas a 0
    request.session["penalty"] = 0



    # Y también enviamos el número de pistas que tiene la pregunta
    cheat_number = Cheat.objects.filter(question=question).count()
    return render(request, 'question/question.html', {
        'question': question,
        'answers': answers,
        'cheat_number': cheat_number,
        'progress': 10, # TODO Calcular el progreso y mostrarlo en un porcentaje?
    })


# Control del guardado de respuestas
# El usuario llega aquí via post tras hacer click en "siguiente pregunta"
@require_http_methods(["POST"])
def save_response(request):
    """ Sólo se guarda la respuesta y se avanza en la pregunta si el usuario la ha respondido """
    actual_question = request.session["actual_question"]
    story_id = request.session["story_id"]
    game_id = request.session["game_id"]
    actual_question_id = request.session["actual_question_id"]

    question = get_object_or_404(Question, pk=actual_question_id)
    story = get_object_or_404(Story, pk=story_id)
    game = get_object_or_404(Game, pk=game_id)

    # Aumentamos el número de intentos
    request.session["attemps_made"] += 1
    attemps = request.session["attemps_made"]
    max_attemps = question.attempts

    # Enlazamos respuesta del usuario y calculamos puntos sólo si la pregunta anterior no era una viñeta
    if question.type != "VINETA":
        print("NO VIÑETA")
        points = 0
        post_answer = ""

        # Comprobamos que el usuario haya incluido una respuesta
        # En caso negativo, la puntuación de la pregunta será cero

        if request.POST.get("answer", ):
            post_answer = request.POST.get("answer", )
            points = 0
            real_answer = ""

            # Buscamos la respuesta real
            if question.type == "TEXTO":
                # answer = get_object_or_404(TextQuestionAnswer, question=question)
                if TextQuestionAnswer.objects.get(question=question):
                    answer = TextQuestionAnswer.objects.get(question=question)

                    # Ponemos ambas, la respuesta del usuario y la original en minúsculas
                    real_answer = answer.answer.lower()
                    post_answer = post_answer.lower()
                else:
                    print("¡Pregunta de texto sin solución!")

            if question.type == "CUESTIONARIO":
                if TestOption.objects.filter(question=question, is_answer=True):
                    answer = TestOption.objects.filter(question=question, is_answer=True).first()
                    real_answer = str(answer.id)

                else:
                    print("Respuesta tipo test sin definir!")

            print(str(real_answer) + " vs " + str(post_answer))



            # Comprobamos intentos
            if attemps < max_attemps and real_answer != post_answer:
                return HttpResponseRedirect(reverse('game:game-controller', ))

            if real_answer == post_answer:
                points = question.points
            else:
                points = 0

            # Restamos los puntos de penalización por haber usado (o no) las pistas y lo reseteamos
            points -= request.session["penalty"]
            request.session["penalty"] = 0


        else:
            # Comprobamos el caso de que el usuario no hay introducido respuesta y le queden intentos
            print("Intentos: " + str(attemps) + " Máximo: " + str(max_attemps))
            if attemps < max_attemps:
                return HttpResponseRedirect(reverse('game:game-controller', ))

        UserAnswer.objects.create_answer(game=game, question=question, answer=post_answer, points=points)




    actual_question += 1
    request.session["actual_question"] = actual_question

    # Guardamos el progreso en la base de datos por si el usuario quiere continuar más tarde
    game.actual_question = actual_question
    game.save()

    if actual_question >= story.get_questions_number():

        # Recopilamos los puntos obtenidos y marcamos variables del final del juego
        game.points = get_game_points_view(game.id)
        game.is_finished = True # Guardando este valor, esta partida será guardada como completada, aunque en un futuro se alteren las preguntas del test

        game.end_date = datetime.now()
        game.save()

        return HttpResponseRedirect(reverse('game:home', ))

    request.session["attemps_made"] = 0
    return HttpResponseRedirect(reverse('game:game-controller', ))


@require_http_methods(["GET"])
def get_cheat(request, question_id, cheat_count):
    question = get_object_or_404(Question, pk=question_id)
    if Cheat.objects.filter(question=question)[int(cheat_count)]:
        # TODO Quitar 1 punto de la pregunta por pista pedida

        request.session["penalty"] += 1
        cheat = Cheat.objects.filter(question=question)[int(cheat_count)]
        return HttpResponse(cheat.text, status=200)
    else:
        return HttpResponse(status=404)

# Función que comprueba si una respuesta es o no correcta en función a la historia y el tipo de pregunta
@require_http_methods(["POST"])
def check_simple_answer(request, answer_text):
    pass

def get_game_points_view(game_id):
    game = get_object_or_404(Game, pk=game_id)
    if UserAnswer.objects.filter(game=game):
        answers = UserAnswer.objects.filter(game=game)
        questions_number = game.story.questions_number
        sum = 0

        for answer in answers:
            sum += answer.points
        sum = sum / questions_number
        return sum  # Devuelve la media de puntuaciones de esta partida en concreto
    else:
        return 0


# Obtiene la puntuación de un juego ya acabado
@require_http_methods(["GET"])
def get_game_points(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if UserAnswer.objects.filter(game=game):
        answers = UserAnswer.objects.filter(game=game)
        questions_number = game.story.questions_number
        sum = 0

        for answer in answers:
            sum += answer.points
        sum = sum / questions_number
        return HttpResponse(sum, status=200) # Devuelve la media de puntuaciones de esta partida en concreto
    else:
        return HttpResponse(status=404)