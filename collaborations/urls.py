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
        "campaign/<int:campaign_pk>/<int:campaign_user_pk>/",
        get_campaign_page,
        name="campaign_page",
    ),
]
