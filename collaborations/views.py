from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from collaborations.models import *
from collaborations.forms import *

from formtools.wizard.views import SessionWizardView

CREATION_FORMS = [
    CampaignCreationStepOneForm,
    CampaignCreationStepTwoForm,
    CampaignCreationStepThreeForm,
    CampaignCreationStepFourForm,
]

# JOINING_FORMS = [CampaignJoiningStepOneForm, CampaignJoiningStepTwoForm]


class CampaignCreationWizardView(SessionWizardView):
    form_list = CREATION_FORMS
    template_name = "collaborations/campaign_creation.html"

    def done(self, form_list, **kwargs):
        pk = self.request.user.pk
        form_data = [form.cleaned_data for form in form_list]
        campaign = Campaign(
            name=form_data[0]["name"],
            start_date=form_data[0]["start_date"],
            end_date=form_data[0]["end_date"],
            description=form_data[1]["description"],
            partner=form_data[2]["partner"],
            collaboration_creator=self.request.user,
        )
        campaign.save()
        # partner_request = CampaignPartnerRequest.objects.create(
        #     campaign=campaign, partner=campaign.partner
        # )
        # partner_request.save()
        messages.success(self.request, "Campagne créée avec succès!")
        return redirect("collaborations:collaborations_list", pk)


@login_required(login_url="users:login")
def create_campaign(request):
    wizard_view = CampaignCreationWizardView.as_view()
    return wizard_view(request)


@login_required(login_url="users:login")
def get_collaborations_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns = Campaign.objects.filter(collaboration_creator=user)
    for campaign in campaigns:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    # collaborations = Campaign.objects.filter(collaborators=user)
    # for campaign in collaborations:
    #     campaign_data = {
    #         "campaign": campaign,
    #         "collaborators": campaign.collaborators.all(),
    #     }
    #     campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns": campaigns,
        "campaign_page_user": user,
    }
    return render(request, "collaborations/campaigns_list.html", context)
