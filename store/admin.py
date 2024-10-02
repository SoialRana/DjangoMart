from django.contrib import admin
from .models import Product,ReviewRating
# Register your models here.

# admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin): #We use modelAdmin when we customize admin panel
    list_display=['product_name','price','category','stock','created_date','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)} # commma dite hobe 
    
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)