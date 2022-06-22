from xml.dom.minidom import Document

from django.urls import path
from . import views
from order.models import Order,Myorder


urlpatterns = [
    path('',views.index,name="index"),
    path('index_2/',views.index_2,name="index_2"),
    path('about',views.about,name="about"),
    path('cart/',views.cart,name="cart"),
    path('contact/',views.contact,name="contact"),
    path('news/',views.news,name="news"),
    path('singleproduct',views.singleProduct,name="singleproduct"),
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('registerotp/',views.register_otp,name='register_otp'),
    path('logout/',views.logoutUser,name='logout'),
    path('viewAccount/',views.viewAccount,name="viewAccount"),
    path('myorder/<str:tno>',views.myorder,name="myorder"),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<slug:category_slug>/', views.shop, name='products-by-category'),
    path('shop/search/', views.search, name='search'),
    path('error/',views.errorpage,name="error"),
    
    
    path('my-account/', views.my_account, name='my-account'),
    path('my-account/my-orders/', views.my_orders, name='my-orders'),
    path('my-account/edit-profile/', views.edit_profile, name='edit-profile'),
    path('my-account/change-password/', views.change_password, name='change-password'),
    path('my-account/my-orders/order-details/<int:order_id>', views.order_details, name='order-details'),
    path('my-account/my-orders/cancel-order/<str:pk>/', views.cancel_order, name='cancel-order'),
   
    
]