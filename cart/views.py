from ast import Return
import logging
from django.contrib import messages
import random

from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from product.models import OrderItem, product, Wishlist
from order.models import Order,Myorder

# Create your views here.
@login_required(login_url='login')
def wishlist(request):
    wishlists  = Wishlist.objects.filter(user=request.user)
    context ={'wishlists':wishlists}
    return render(request,'wishlist.html',context)


@login_required(login_url='login')
def viewcart(request):
        cart =OrderItem.objects.filter(user = request.user)
        total=0
        for item in cart:
           total += item.product.price * item.quantity 
        context ={'cart':cart , 'total':total}
        return render(request,"cart.html",context)
   

def addtocart(request):
    if request.user.is_authenticated:
        if request.POST.get('action')== 'POST':
            prod_id = request.POST['productid']
            prod_qty = request.POST['productqty']
            
            product_check = product.objects.get(id=prod_id)
            if product_check:
                if OrderItem.objects.filter(user=request.user.id,product_id=prod_id):
                    return JsonResponse({'status':"Product Already in cart"})
                else:
                    
                    if product_check.stock >= int(prod_qty):
                        OrderItem.objects.create(user=request.user, product_id=prod_id , quantity=prod_qty)
                        return JsonResponse({'status':"Product added successfully"})
                    else:
                        return JsonResponse({'status':"Only" + str(product_check.stock)+ "stock available"})
            else:
                return JsonResponse({'status':"no such product found"})
        else:
            return JsonResponse({'status':"login required"})
    return redirect('index')


def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))

        if OrderItem.objects.filter(user=request.user,product_id=prod_id):
            prod_qty = int(request.POST.get('quantity'))
            cart = OrderItem.objects.get(  product_id=prod_id ,user=request.user)
            cart.quantity=prod_qty
            cart.save()
            return JsonResponse({'status':"updated"})
    return redirect('index')

def remove_cart (request,product_id):
    user = request.user
    if user.is_authenticated:
        Product = get_object_or_404(product,id=product_id)
        cart_item=OrderItem.objects.get(product=Product , user= request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('viewcart')
def add_quantity(request,product_id):
    user = request.user
    if user.is_authenticated:
        Product = get_object_or_404(product,id=product_id)
        cart_item=OrderItem.objects.get(product=Product , user= request.user)
        if cart_item.quantity < 5:
            cart_item.quantity +=1
            cart_item.save()
        else:
            messages.error(request," 5 is the limit")
        return redirect('viewcart')

def delete_cart(request,product_id):
    current_user=request.user
    if current_user.is_authenticated:
        product_id=get_object_or_404(product,id=product_id)
        cart_item =  OrderItem.objects.get (  product=product_id, user=request.user )
        cart_item.delete()
        return redirect ('viewcart')
    
def add_to_wishlist(request):
        if request.user.is_authenticated:
          if request.POST.get('action')=='POST':
            prod_id = request.POST['product_id']
            
            item = product.objects.get(id = prod_id)
            try:
                wishlist_items=Wishlist.objects.get(
                    user=request.user, product=item
                )
            except Wishlist.DoesNotExist:
                wishlist_items=Wishlist.objects.create(
                    user=request.user,product=item
                )
                wishlist_items.save()
        return redirect('index')
    
    
def delete_wishlist(request,pk):
    user=request.user
    if user.is_authenticated:
        item = product.objects.get(id = pk)
        wish_item = Wishlist.objects.get(product = item)
        wish_item.delete()
        
        return redirect('wishlist')
    
    return redirect('wishlist')


@login_required(login_url='login')
def checkout(request): 
    rawcart = OrderItem.objects.filter(user=request.user )
    for item in rawcart:
        if item.product.available ==False:
            OrderItem.objects.delete(id=item.id)
    cartitem = OrderItem.objects.filter(user=request.user)
    total_price = 0
    for item in cartitem:
        total_price += item.quantity * item.product.price
    return render(request,'checkout.html',{'cartitem':cartitem,'total':total_price})

           
            
        
        
        
        
        
