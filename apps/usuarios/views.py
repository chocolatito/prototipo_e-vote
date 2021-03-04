# from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

# depends de apps.index
# Create your views here.


class LoginFormView(LoginView):
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Iniciar Sesión"
        return context


def logout_view(request):
    logout(request)
    return redirect('index:index')
