from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('manager', 'Fridge Manager'),
        ('member', 'Member'),
    ]

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    @property
    def is_fridge_manager(self):
        return self.role == 'manager' or self.is_superuser

    def __str__(self):
        return self.username


class FridgeItem(models.Model):

    class StorageZone(models.TextChoices):
        FRIDGE = 'fridge', 'Fridge'
        FREEZER = 'freezer', 'Freezer'
        PANTRY = 'pantry', 'Pantry / Door'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fridge_items',
    )
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=60, blank=True)
    zone = models.CharField(
        max_length=20,
        choices=StorageZone.choices,
        default=StorageZone.FRIDGE,
    )
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=30, default='pcs')
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expiry_date', '-created_at']

    def __str__(self):
        return f'{self.name} ({self.quantity} {self.unit})'