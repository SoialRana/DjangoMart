from django.contrib import admin
from .models import Product
# Register your models here.

# admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin): # adminn panel customize korte ModelAdmin use kori 
    list_display=['product_name','price','category','stock','created_date','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)} # commma dite hobe ... prepopulated_field ta oi jonno use kora hoi jeno automatically generate hoi slag ta ei jonno
    
admin.site.register(Product,ProductAdmin)