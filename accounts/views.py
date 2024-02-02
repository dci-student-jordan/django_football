from typing import Any
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from templates.shared import shop_link, team_site, top_links
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.views.generic.edit import FormView
from eshop.models import Order


class LoginView(FormView):
    template_name = 'registration/signupdate.html'
    form_class = LoginForm
    success_url = reverse_lazy("eshop_home")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            # Handle invalid login
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["extra_style"] = "accounts/style.css"
        context["navs"] = mark_safe(top_links(reverse("update", args=[0]), ["team", "eshop"]))
        context["foot"] = mark_safe(team_site()+shop_link())
        context["Action"] = "Log in"
        return context



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("eshop_home")
    template_name = "registration/signupdate.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Log in the user after successful registration
        login(self.request, self.object)

        return response
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["extra_style"] = "accounts/style.css"
        context["navs"] = mark_safe(top_links(reverse("update", args=[0]), ["team", "eshop"]))
        context["foot"] = mark_safe(team_site()+shop_link())
        context["Action"] = "Sign up"
        return context
    
class UpdateUserView(LoginRequiredMixin, UpdateView):

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print("GET:", request)
        if self.get_object().pk != request.user.pk:
            return redirect('login')
        return super().get(request, *args, **kwargs)
    
    model = User
    success_url = reverse_lazy("eshop_home")
    template_name = "registration/signupdate.html"
    fields = ('username', 'first_name', 'last_name', 'email')
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["extra_style"] = "accounts/style.css"
        context["navs"] = mark_safe(top_links(reverse("update", args=[0]), ["team", "eshop"]))
        context["foot"] = mark_safe(team_site()+shop_link())
        context["Action"] = "Update"
        user_activities = Order.objects.filter(user_id=self.request.user.id)
        print(user_activities)
        context["user_activities"] = [f"Bought a {act}" for act in user_activities]
        return context