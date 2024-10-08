from django.urls import path
from collaborations.views import *

app_name = "collaborations"

urlpatterns = [
    path(
        "collaborations_list/<int:pk>",
        get_collaborations_list,
        name="collaborations_list",
    ),
    path(
        "campaign_creation/",
        create_campaign,
        name="campaign_creation",
    ),
    path(
        "campaign/<int:campaign_pk>/<int:campaign_user_pk>",
        get_campaign_page,
        name="campaign_page",
    ),
    path(
        "join_campaign/<int:campaign_pk>/",
        join_campaign,
        name="join_campaign",
    ),
    path(
        "collaborator_requests_list",
        collaborator_requests,
        name="collaborator_requests",
    ),
    path(
        "partners_requests_list",
        partner_requests,
        name="partners_requests",
    ),
    path(
        "accept_collaborator_request/<int:request_id>/",
        accept_collaborator_request,
        name="accept_collaborator_request",
    ),
    path(
        "refuse_collaborator_request/<int:request_id>/",
        refuse_collaborator_request,
        name="refuse_collaborator_request",
    ),
    path(
        "accept_partner_request/<int:request_id>/",
        accept_partner_request,
        name="accept_partner_request",
    ),
    path(
        "refuse_partner_request/<int:request_id>/",
        refuse_partner_request,
        name="refuse_partner_request",
    ),
    # path(
    #     "campaigns/create/<int:collaborator_id>/",
    #     create_campaign,
    #     name="campaign_creation_with_collab",
    # ),
    # path(
    #     "campaigns/create/",
    #     create_campaign,
    #     name="campaign_creation",
    # ),
    # path("campaigns_list/<int:pk>/", get_campaigns_list, name="campaigns_list"),
    # path(
    #     "campaigns_participate_list/<int:pk>/",
    #     get_campaigns_participate_list,
    #     name="campaigns_participate_list",
    # ),
    # path(
    #     "campaigns_created_list/<int:pk>/",
    #     get_campaigns_created_list,
    #     name="campaigns_created_list",
    # ),
    # path(
    #     "accept_campaign_collaborator_request/<int:request_id>/",
    #     accept_campaign_collaborator_request,
    #     name="accept_campaign_collaborator_request",
    # ),
    # path(
    #     "refuse_campaign_collaborator_request/<int:pk>/",
    #     refuse_campaign_collaborator_request,
    #     name="refuse_campaign_collaborator_request",
    # ),
    # path(
    #     "join_campaign/<int:campaign_pk>/<int:campaign_user_pk>/",
    #     join_campaign,
    #     name="join_campaign",
    # ),
]
