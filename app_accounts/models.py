from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=100)
    is_email_varified = models.models.BooleanField(default=False)
    email_token = models.models.CharField(max_length=100, null=True, blank=True)
    