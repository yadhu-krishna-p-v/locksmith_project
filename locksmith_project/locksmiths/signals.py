from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LocksmithProfile
from users.models import User

@receiver(post_save, sender=User)
def create_locksmith_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'locksmith':
        LocksmithProfile.objects.create(user=instance)
