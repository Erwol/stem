from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import login
from django.views.generic import FormView, ListView, DetailView, CreateView, DeleteView, UpdateView



def custom_login(request, **kwargs):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('game:home'))
    else:
        return login(request, **kwargs)