import os.path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from .models import CustomUser


class Signup(View):
    form = UserRegistrationForm
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:flux')

        return render(request, self.template_name, {'form': form})


class Profile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "registration/profile.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.id == kwargs['pk']:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('blog:flux')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = CustomUser.objects.get(pk=self.object.pk)
        return context


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        #url = super().get_success_url()
        return os.path.join("/accounts/profile/", str(self.request.user.pk))


class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"






