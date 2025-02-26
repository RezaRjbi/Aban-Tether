from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from typing import TYPE_CHECKING

from .models import Balance

if TYPE_CHECKING:
    from users.models import User

UserModel: "User" = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.get_or_create(user=instance)
