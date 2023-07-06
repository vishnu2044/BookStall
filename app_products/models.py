from django.db import models
from app_category.models import Category_list
from app_authors.models import Authors
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    product_description = models.TextField(max_length=300, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    images = models.ImageField(default=True, upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category_list, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def is_outofstock(self):
        return self. stock <=0
    
    def get_url(self):
        return reverse('product_details',args = [self.slug])

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'product')

