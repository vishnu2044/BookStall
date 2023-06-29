from django.db import models
from base.models import BaseModel

# Create your models here.

class Authors(BaseModel):
    Author_name = models.CharField(max_length=255)
    Author_quotes = models.TextField()
    Author_description = models.TextField()
    Author_image = models.ImageField()
