from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    """Custom user manager to handle role field"""
    def create_user(self, username, email, password=None, role='customer'):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('locksmith', 'Locksmith'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    # Fix related_name conflicts
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    objects = UserManager()  # Use the custom manager

    def __str__(self):
        return self.username
