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
]
