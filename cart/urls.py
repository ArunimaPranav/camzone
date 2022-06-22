from django.urls import path
from django.urls.resolvers import URLPattern
from . import views



urlpatterns=[
    path('add-to-cart/',views.addtocart,name="add-to-cart"),
    path('viewcart/update-cart',views.updatecart,name="update-cart"),
    path('delete-cart/<str:product_id>',views.delete_cart,name="delete-cart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('addtowishlist/',views.add_to_wishlist,name="addtowishlist"),
    path('delete-wishlist/<str:pk>/',views.delete_wishlist,name="delete-wishlist"),
   
    path('checkout/',views.checkout,name="checkout"),
    path('removecart/<str:product_id>/',views.remove_cart,name="removecart"),
    path('addquantity/<str:product_id>/',views.add_quantity,name="addquantity")
]