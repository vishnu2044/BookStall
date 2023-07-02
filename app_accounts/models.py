from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)


