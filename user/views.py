from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import login, logout
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView

from user.forms import UserForm
from user.models import User


def custom_login(request, **kwargs):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('game:home'))
    else:
        return login(request, **kwargs)

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:index'))

class UserCreateView(FormView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy('user:index')
    form_class = UserForm

    def form_valid(self, form):
        user = User.objects.create_user(
                password=form.cleaned_data['password'],
                username=form.cleaned_data['username']
        )
        return super(UserCreateView, self).form_valid(form)