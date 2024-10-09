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

JOINING_FORMS = [CampaignJoiningStepOneForm, CampaignJoiningStepTwoForm]


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
        partner_request = PartnerRequest.objects.create(
            campaign=campaign, partner=campaign.partner
        )
        partner_request.save()
        messages.success(self.request, "Campagne créée avec succès!")
        return redirect("collaborations:collaborations_list", pk)


class CampaignJoiningWizardView(SessionWizardView):
    form_list = JOINING_FORMS
    template_name = "collaborations/campaign_joining.html"

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        collaboration_request = CollaboratorRequest(
            message=form_data[0]["message"],
            campaign=self.kwargs.get("campaign"),
            collaborator=self.request.user,
        )

        collaboration_request.save()
        messages.success(self.request, "Demande de participation envoyer !")
        return redirect("home")


@login_required(login_url="users:login")
def create_campaign(request):
    wizard_view = CampaignCreationWizardView.as_view()
    return wizard_view(request)


@login_required
def join_campaign(request, campaign_pk):

    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    # campaign_page_user = get_object_or_404(CustomUser, pk=campaign_user_pk)
    wizard_view = CampaignJoiningWizardView.as_view()
    return wizard_view(request, campaign=campaign)


@login_required(login_url="users:login")
def get_collaborations_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns_created = Campaign.objects.filter(collaboration_creator=user)
    for campaign in campaigns_created:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    collaborations = Campaign.objects.filter(collaborators=user)
    for campaign in collaborations:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    print(context)
    return render(request, "collaborations/campaigns_list.html", context)


@login_required(login_url="users:login")
def get_collaborations_participate_list(request, pk):
    campaigns_with_collaborators = []
    user = get_object_or_404(CustomUser, pk=pk)

    collaborations = Campaign.objects.filter(collaborators=user)
    for campaign in collaborations:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "collaborations/campaigns_list.html", context)


@login_required(login_url="users:login")
def get_collaborations_created_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns_created = Campaign.objects.filter(collaboration_creator=user)
    for campaign in campaigns_created:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "collaborations/campaigns_list.html", context)


@login_required(login_url="users:login")
def get_campaign_page(request, campaign_pk, campaign_user_pk):

    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    user = get_object_or_404(CustomUser, pk=campaign_user_pk)

    context = {
        "campaign": campaign,
        "campaign_page_user": user,
    }
    return render(request, "collaborations/campaign_page.html", context)


@login_required(login_url="users:login")
def collaborator_requests(request):
    user = request.user
    user_campaigns = Campaign.objects.filter(
        collaboration_creator=user
    )
    requests = []
    collaboration_requests = CollaboratorRequest.objects.all()
    for campaign in user_campaigns:
        for collaboration_request in collaboration_requests:
            if collaboration_request.campaign == campaign and collaboration_request.status == "pending":
                requests.append(collaboration_request)

    context = {
        "requests": requests,
        "campaign_page_user": user,
    }
    return render(request, "collaborations/collaboration_requests_list.html", context)


@login_required(login_url="users:login")
def accept_collaborator_request(request, request_id):
    request_obj = CollaboratorRequest.objects.get(pk=request_id)
    campaign = get_object_or_404(Campaign, id=request_obj.campaign_id)
    request_obj.status="accepted"
    campaign.add_collaborator(request_obj.collaborator)
    campaign.save()
    request_obj.save()
    messages.info(request, "Paiement éffectué !")
    return redirect("home")


@login_required
def refuse_collaborator_request(request, request_id):
    request_obj = CollaboratorRequest.objects.get(pk=request_id)
    request_obj.status = "rejected"
    request_obj.save()
    return redirect("home")


@login_required(login_url="users:login")
def partner_requests(request):
    user = request.user
    partner_requests = PartnerRequest.objects.filter(partner=user, status="pending")
    context = {"requests": partner_requests, "campaign_page_user": user}
    return render(request, "collaborations/collaboration_requests_list.html", context)


@login_required(login_url="users:login")
def accept_partner_request(request, request_id):
    request_obj = PartnerRequest.objects.get(pk=request_id)
    request_obj.status = "accepted"
    request_obj.save()
    messages.info(request, "Paiement éffectué !")
    return redirect("home")


@login_required
def refuse_partner_request(request, request_id):
    request_obj = PartnerRequest.objects.get(pk=request_id)
    campaign = get_object_or_404(Campaign, id=request_obj.campaign_id)
    campaign.remove_partner()
    request_obj.status = "rejected"
    campaign.save()
    request_obj.save()
    return redirect("home")
