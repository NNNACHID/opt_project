import json
from django import forms
from django.utils.translation import gettext_lazy as _
from collaborations.models import Campaign
from users.models import CustomUser


class CampaignCreationStepOneForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ["name", "start_date", "end_date"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": _("Nom de la campagne"),
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "input",
                    "placeholder": _("Début de la campagne"),
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "class": "input",
                    "placeholder": _("Fin de la campagne"),
                }
            ),
        }

        labels = {
            "name": _("Nom de la campagne"),
            "start_date": _("Début"),
            "end_date": _("Fin"),
        }

class CampaignCreationStepTwoForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = [
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "",
                    "placeholder": "Descriptif de la campagne (facultatif)",
                }
            )
        }

class CampaignCreationStepThreeForm(forms.Form):

    partner = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="advertiser"),
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
        label="Partenaire",
    )

    class Meta:
        model = Campaign
        fields = ["partner"]

class CampaignCreationStepFourForm(forms.Form):

    accept_legal_terms = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "radio"}
        ),
        required=True,
    )
