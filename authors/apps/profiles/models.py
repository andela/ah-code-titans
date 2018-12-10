
from django.db import models
from ..authentication.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    create a user profile model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, blank=False)
    bio = models.TextField(blank=True)
    image = models.URLField(
        blank=True,
        default="https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png"
    )
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=100, blank=True)
    location = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    create profile upon user registration.
    """
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save created user profile.
    """
    instance.profile.save()
