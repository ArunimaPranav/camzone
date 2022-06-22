from django import urls
from  django.urls import path
from product import views



urlpatterns= [
    path ('addproduct',views.add_product,name="add_product"),
    path('view_product/<slug:slug>/',views.view_product,name="viewproduct"),
    
]