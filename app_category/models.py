from django.db import models


# Create your models here.
class Category_list(models.Model):
    category_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, blank= True)
    category_description = models.TextField()
    is_available = models.BooleanField(default=False)



    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
