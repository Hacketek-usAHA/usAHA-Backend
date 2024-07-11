from django.db import models
from django.conf import settings
import uuid

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.user.username
