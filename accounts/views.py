from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LeebUserSignUpForm


class SignUpView(CreateView):
    form_class = LeebUserSignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
