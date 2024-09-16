from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from collaborations.models import *
from collaborations.forms import *

from formtools.wizard.views import SessionWizardView


@login_required(login_url="users:login")
def get_campaigns_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns_created = Campaign.objects.filter(campaign_creator=user)
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
        "campaigns_with_collaborators": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "campaigns_list.html", context)
