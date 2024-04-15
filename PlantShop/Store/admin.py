from django.contrib import admin
from Store.models import Category,Product
# Register your models here.


#In Django, the admin.site.register() function is used to register a model with the Django admin interface.
admin.site.register(Category)
admin.site.register(Product)
