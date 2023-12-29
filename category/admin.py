from django.contrib import admin
from .models import Category
# Register your models here.
# admin.site.register(Category)

# As I have create a model admin so at first i create a customize admin panel. This work i have done for slug field
class CategoryAdmin(admin.ModelAdmin):
    # If i anything write something then prepopulated field generate automatically
    prepopulated_fields={'slug': ('category_name',)} # I make slug from model field
    # prepopulated fields must be tuple so that we use comma otherwise it make some errors
    list_display=('category_name','slug') # I want to add category name in the slug field

admin.site.register(Category,CategoryAdmin)
# If i want to createsuperuser first must be i have done makemigration and migrate
