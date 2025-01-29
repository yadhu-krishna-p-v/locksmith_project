from django.db import models


class LocksmithProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='locksmith_profile')
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return self.business_name
