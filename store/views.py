

from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from order.models import Myorder
from django.contrib.auth.decorators import login_required
from store.otp import send_otp, verify_otp
from.forms import RegistrationForm, UserForm, UserProfileForm
from.models import Account, Address, UserProfile
from django.contrib import messages,auth
from django.contrib.auth import authenticate,logout
import os
from product.models import Category,product
from order.models import Order,Myorder

from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def registerPage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            
            user = Account.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, gender=gender, mobile=mobile, password=password)
            user.save()
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
            request.session['mobile']=mobile
            send_otp(mobile)
            print(mobile)
            # messages.success(request,'Registration Successful')
            return redirect('register_otp')
    form=RegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request) 
    return redirect('index')

def register_otp(request):
    if request.method == 'POST':
        check_otp = request.POST.get('otp')
        print(check_otp)
        mobile=request.session['mobile']
        check=verify_otp(mobile,check_otp)
        if check:
            user = Account.objects.get(mobile = mobile)
            user.is_verified = True
            user.save()
            return redirect('index')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('register_otp')
    return render(request,'register_otp.html')
def about(request):
    context={}
    return render(request,'about.html',context)
def index(request):
    products = product.objects.all()
    return render(request,'index.html',{'products':products})
def index_2(request):
    context={}
    return render(request,'index_2.html',context)
def cart(request):
    context={}
    return render(request,'cart.html',context)
def checkout(request):
    context={}
    return render(request,'checkout.html',context)

def singleProduct(request):
    context={}
    return render(request,'single-product.html',context)
def singlenews(request):
    context={}
    return render(request,'single-news.html',context)

def contact(request):
    context={}
    return render(request,'contact.html',context)
def news(request):
    context={}
    return render(request,'news.html',context)
def errorpage(request):
    context={}
    return render(request,'404.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        if email == '' and password == '':
           messages.error(request,"please provide an email and  password")
        elif password == '' :
            messages.error(request,"enter password")
        elif email == '' :
            messages.error(request, 'please  provide an email')
        else:
            try:
                user = Account.objects.get(email=email)
                print(user)
            except:
                messages.error(request,"user does not exist")
            
        
        
        
        user = authenticate(request,email=email,password=password)
        
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'user or password does not match..')
    
    return render(request,'login.html')

def viewAccount(request):
    addresses   =  Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    context={'addresses':addresses,'orders':orders}
    return render(request,'view_Account.html',context)

def myorder(request,tno):
    order= Order.objects.filter(user=request.user,tracking_no=tno).first()
    orderitem = Myorder.objects.filter(order=order)
    context ={'orderitem':orderitem , 'order':order}
    return render(request,"viewmyorder.html",context)


def shop(request, category_slug=None) :
    categories = None
    products = None
    
    if category_slug is not None :
        categories = get_object_or_404(Category, slug=category_slug)
        products = product.objects.filter(category=categories, available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else :
        products = product.objects.all().filter(available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
        
    context = {
        
        # for paginations, instead of passing the whole products, only pass paged products which will be 6 in this case.
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request, 'shop.html', context)
def search(request) :
    
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword :
            products = product.objects.filter(name__icontains = keyword)
            
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        else :
            products = product.objects.all().filter(available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count
    }
    return render(request, 'shop.html', context)


""" USER PROFILE """
@login_required(login_url='login')
def my_account(request) :
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    order_items = Myorder.objects.filter(order=orders)
    user_profile = UserProfile.objects.get(user_id=request.user.id)
   
    context = {
        'addresses' : addresses,
        'orders' : orders,
        'order_items' : order_items,
        'orders_count' : orders_count,
        'user_profile' : user_profile,
    }
    return render(request, 'my-account.html', context)

@login_required(login_url='login')
def my_orders(request) :
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders
    }
    return render(request, 'my-orders.html', context)


@login_required(login_url='login')
def edit_profile(request) :
    
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST' :
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit-profile')
    else :    
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)    
    
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'user_profile' : user_profile,
    }
    
    return render(request, 'edit-profile.html', context)

@login_required(login_url='login')
def change_password(request) :
    if request.method == 'POST' :
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact = request.user.email)
        
        if new_password == confirm_password :
            success = user.check_password(current_password)
            if success :
                user.set_password(new_password)
                user.save()
                
                # logout(request) 
                
                messages.success(request, 'Password changed successfully')
                return redirect('my-account')
            else :
                messages.error(request, 'Please enter correct Current Password')
                return redirect('change-password')
        else :
            messages.error(request, 'New Password Does Not Match')
            return redirect('change-password')
        
    
    return render(request, 'change-password.html')


@login_required(login_url='login')
def order_details(request, order_id) :
    order_details = Myorder.objects.filter(order__tracking_no=order_id).order_by('-created_at')
    order = Order.objects.get(tracking_no=order_id)
    
    context = {
        'order_details' : order_details,
        'order' : order,
    }
    
    return render(request, 'order-details.html', context)


@login_required(login_url='login')
def cancel_order(request, pk):
    cancel_product = Myorder.objects.get(id=pk)
    cancel_product.status = 'cancelled'
    cancel_product.save()
    
    product_id = cancel_product.product.id
    
    products = product.objects.get(id=product_id)
    products.stock += cancel_product.quantity
    products.save()
    
    return redirect('my-orders')

    
       