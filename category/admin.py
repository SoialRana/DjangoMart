from django.contrib import admin
from .models import Category
# Register your models here.
# admin.site.register(Category)

# amader ekta model admin make korte hobe jodi ekta customize admin panel chay
# ei kaj ti slug er jonno korte hoi 

class CategoryAdmin(admin.ModelAdmin):
    # ami ja likhbo prepopulated_field automatic kisu zenarate korbe ...
    prepopulated_fields={'slug': ('category_name',)} # model name theke slug toiri korte chay
    # prepopulated fields must be tuple ei jonno amader comma use korte hobe na hole error khabo 
    list_display=('category_name','slug') # ami chay slug field er moddhe category name ta chole asuk

admin.site.register(Category,CategoryAdmin)
# create superuser korar age sob somoy makemigration and migrate korte hobe 

