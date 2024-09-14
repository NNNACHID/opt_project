from django.db import models
from django.conf import settings
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("creator", "Creator"),
        ("advertiser", "Advertiser"),
        ("association", "Association"),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="creator")

DEFAULT_BANNER_PATH = "banners/default_banner.jpg"
DEFAULT_PROFILE_PICTURE_PATH = "profile_pictures/default-profile-picture.jpg"
TEXT_FIELD_OPTIONS = {
    "null": True,
    "blank": True,
}


class SocialMediaLinks(models.Model):
    instagram_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="Instagram"
    )
    x_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="X (Twitter)"
    )
    youtube_channel_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="YouTube"
    )
    twitch_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="Twitch"
    )
    tiktok_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="TikTok"
    )
    snapchat_url = models.URLField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="Snapchat"
    )

    def __str__(self):
        return f"Social Media Links for {self.id}"


class CustomUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=255, unique=True, default="SOME STRING")
    title = models.TextField(
        verbose_name="Short description",
        help_text="Enter a short description",
        **TEXT_FIELD_OPTIONS
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description",
        **TEXT_FIELD_OPTIONS
    )
    partners = models.JSONField(default=dict)

    banner = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True,
        default=DEFAULT_BANNER_PATH,
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        default=DEFAULT_PROFILE_PICTURE_PATH,
    )

    social_media_links = models.OneToOneField(
        SocialMediaLinks, on_delete=models.CASCADE, null=True, blank=True
    )

    contact_mail = models.EmailField(
        max_length=255, **TEXT_FIELD_OPTIONS, verbose_name="Adresse e-mail"
    )

    def __str__(self):
        return self.name
