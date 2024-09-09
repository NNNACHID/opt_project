from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)

from users.models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ["password1", "password2"]:
            self.fields[field_name].widget.attrs.update(
                {"class": "form-control form-control-lg"}
            )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label="",
        required=True,
        widget=forms.RadioSelect(
            attrs={"class": "form-check-input form-check-inline", "type": "radio"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = [
            "role",
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Identifiant",
                    "class": "form-control form-control-lg",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control form-control-lg"}
            ),
            "role": forms.CheckboxInput(
                attrs={"class": "form-check-input", "type": "radio"}
            ),
            "password1": forms.PasswordInput(
                attrs={
                    "placeholder": "Mot de passe",
                    "class": "form-control form-control-lg",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control form-control-lg"}
            ),
        }


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Identifiant",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control"}
            ),
        }
