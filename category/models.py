from django.db import models

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    #ekta url name k amra define or customize kortechi and jodi multiple word thake oi url e 
    # sekhetre shob nam gulo choto hater kore dicchi and majher space k _ diye replace kortechi 
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True) #blank mane diteo pare na diteo pare
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)
    
    def __str__(self):
        return self.category_name # amader obj gulor nam tar nam onusare hobe 