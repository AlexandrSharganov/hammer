import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def generate_invite_code(sender, instance, **kwargs):
    if not instance.invite_code:
        while True:
            invite_code = str(uuid.uuid4())[:6]
            if not User.objects.filter(invite_code=invite_code).exists():
                instance.invite_code = invite_code
                break
