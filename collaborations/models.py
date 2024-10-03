from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Collaboration(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    collaboration_creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_campaigns"
    )

    class Meta: 
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="end_date_must_be_after_start_date",
            ),
        ]


class Campaign(Collaboration):
    is_open = (
        models.BooleanField(
            default=True,
        ),
    )
    collaborators = models.ManyToManyField(
        CustomUser, related_name="campaigns_participated"
    )
    partner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="campaign_partner",
        limit_choices_to={"role": "advertiser"},
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.name

    def add_collaborator(self, collaborator):
        self.collaborators.add(collaborator)

    def remove_collaborator(self, collaborator):
        self.collaborators.remove(collaborator)

class CollaborationRequest(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_("Message"), null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True


class PartnerRequest(CollaborationRequest):
    partner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class CollaboratorRequest(CollaborationRequest):
    collaborator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
