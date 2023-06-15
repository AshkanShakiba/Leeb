from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import LeebUser


class LeebUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = LeebUser
        fields = UserCreationForm.Meta.fields + ("email", "credit",)


class LeebUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = LeebUser
        fields = UserChangeForm.Meta.fields


class LeebUserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = LeebUser
        fields = UserCreationForm.Meta.fields + ("email",)
