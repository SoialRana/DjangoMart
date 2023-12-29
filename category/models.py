from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    # We define or customize url name and if it have multiple word in this url name then every letter must be small 
    # letter and use underscore instead of space
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True) #blank means it can be null
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)
    
    # def __str__(self):
    #     return self.category_name # Object name must be according to category name 
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    def __str__(self):
        return self.category_name