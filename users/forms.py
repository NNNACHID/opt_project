from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)

from users.models import CustomUser, CustomUserProfile

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
        
        labels = {
            
        }

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


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Identifiant",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Identifiant",
                "class": "input input-bordered",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "input input-bordered"}
        ),
    )


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

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
        }


class CustomUserProfileForm(forms.ModelForm):

    class Meta:

        model = CustomUserProfile

        fields = [
            "banner",
            "profile_picture",
            "title",
            "description",
            "contact_mail",
        ]

        widgets = {
            "banner": forms.FileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full max-w-xs",
                    "type": "file",
                }
            ),
            "profile_picture": forms.FileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full max-w-xs",
                    "type": "file",
                }
            ),
            "title": forms.Textarea(
                attrs={"class": "textarea", "rows": "1", "maxlength": "64"}
            ),
            "description": forms.Textarea(attrs={"class": "textarea", "rows": "3"}),
            "contact_mail": forms.EmailInput(
                attrs={
                    "placeholder": "Email de contact",
                    "class": "input input-bordered",
                    "type": "email",
                }
            ),
        }
