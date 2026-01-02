from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('SUPERADMIN', 'Super Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_banned = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    @property
    def is_admin_or_superadmin(self):
        return self.role in ('ADMIN', 'SUPERADMIN') or self.is_superuser

    def __str__(self):
        return self.username