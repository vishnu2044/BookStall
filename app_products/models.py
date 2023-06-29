from django.db import models
from base.models import BaseModel
from app_category.models import Category
from app_authors.models import Authors


# Create your models here.

class product(BaseModel):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank= True)
    product_description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)


class ProductImage(BaseModel):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product')

