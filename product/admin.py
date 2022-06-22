from unicodedata import category
from django.contrib import admin

from .models import *

class ProductAdmin(admin.ModelAdmin) :
    # To autogenerate slug
    prepopulated_fields = {'slug' : ('name',)}
    
    list_display = ('name', 'category', 'price', 'stock', 'available')


class CategoryAdmin(admin.ModelAdmin) :
    list_display = ('category_name', 'slug')
    
    # To autogenerate slug
    prepopulated_fields = {'slug' : ('category_name',)}

# Register your models here.
admin.site.register(product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(OrderItem)
admin.site.register(Wishlist)

