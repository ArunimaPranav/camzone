from datetime import datetime
from distutils.command.upload import upload
from email import message
from turtle import mode
from unicodedata import category, name
from venv import create
from django.db import models
from store.models import *
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


#category model where different categories where stored
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True, null=True, blank=True)
    
    # slug in Django Admin
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    
    
    # to auto generate slug on our Admin
    def save(self, *args, **kwargs) :
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    
    # To get url and to give it on the a tag href
    def get_url(self) :
        return reverse('products-by-category', args=[self.slug])
        
        
    # To fix Plural of category in admin side
    class Meta :
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.category_name
    
class product (models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    desc=models.TextField()
    price=models.FloatField(default=0.0)
    stock=models.IntegerField(default=0)
    img=models.ImageField(upload_to='images/')
    img1=models.ImageField(upload_to='images/',null=True,blank=True)
    img2=models.ImageField(upload_to='images/',null=True,blank=True)
    available = models.BooleanField(default=True)

      # to auto generate slug on our Admin
    def save(self, *args, **kwargs) :
        self.slug = slugify(self.name)
        super(product, self).save(*args, **kwargs)
        
    
    def get_url(self) :
        return reverse('product-details', args=[self.category.slug, self.slug])
 
    def __str__(self):
        return self.name 
    



class OrderItem(models.Model):
    user          =   models.ForeignKey(Account,on_delete = models.CASCADE , blank=True ,null=True)
    product       =   models.ForeignKey(product,on_delete = models.CASCADE)
    ordered      =   models.BooleanField(default=False,null=True,blank=False)
    quantity      =   models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"
    def get_total_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_price()

    
class Wishlist(models.Model):
    user =   models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name






    
    
     
 
     
    

    
        
    
    
    
        
        
          