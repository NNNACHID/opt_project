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
                {
                    "class": "input input-bordered",
                    "placeholder": "Mot de passe"
                }
            )

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label="",
        required=True,
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
                    "class": "input input-bordered",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "input input-bordered"}
            ),
            "role": forms.CheckboxInput(
                attrs={"class": "radio-primary", "type": "radio"}
            ),
            "password1": forms.PasswordInput(
                
            ),
            "password2": forms.PasswordInput(),
        }


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

        # widgets = {
        #     "username": forms.TextInput(
        #         attrs={
        #             "placeholder": "Identifiant",
        #             "class": "form-control",
        #         }
        #     ),
        #     "email": forms.EmailInput(
        #         attrs={"placeholder": "Email", "class": "form-control"}
        #     ),
        # }
