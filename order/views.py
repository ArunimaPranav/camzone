from django.shortcuts import render, redirect
from product.models import OrderItem
from .forms import OrderForm, PaymentForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from product.models import *
import datetime
import razorpay


# Create your views here.
@login_required(login_url='login')
def place_order(request, total=0, quantity=0) :
    current_user = request.user
    
    # if the cart count is less than or equal to zero, then redirect back to shop
    cart_items = OrderItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0 :
        return redirect('shop')
    
    grand_total, tax = 0, 0
    
    for cart_item in cart_items :
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        print(cart_item)  
    tax = (5 * total) / 100
    grand_total = total + tax    
    
    
    if request.method == 'POST' :
        form = OrderForm(request.POST)
        
        if form.is_valid() :
            # store all the billing information inside Order table
            new_order = Order.objects.create(
            user = current_user,
            full_name = request.POST['full_name'],
            address = request.POST['address'],
            city = request.POST['city'],
            pin_code = request.POST['pin_code'],
            state = request.POST['state'],
            country = request.POST['country'],
            mobile = request.POST['mobile'],
            # message = request.POST['message'],
            landmark = request.POST['landmark'],
            total_price = grand_total,
            tax = tax,
            ip = request.META.get('REMOTE_ADDR'),
            )
        
            
            # To generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            
            tracking_no = current_date + str(new_order.id)
            new_order.tracking_no = tracking_no
            new_order.save()
            
            order = Order.objects.get(user=current_user, is_ordered = False, tracking_no=tracking_no)
            
            request.session['tracking_no'] = tracking_no
            
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            return render(request,'payment.html', context)
        
        
        else :
            
            return redirect('checkout')
        

@csrf_exempt
def payments(request):
    total, quantity = 0, 0
    current_user = request.user
    order_id = request.session['tracking_no']
    order = Order.objects.get(tracking_no = order_id)
    cart_items =OrderItem.objects.filter(user=current_user)
    
    for cart_item in cart_items :
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    tax = (5 * total) / 100
    grand_total = total + tax

    if request.method == 'POST' :
        
        name = current_user.first_name
        email = current_user.email
        amount = grand_total * 100



        # create razorpay client
        client =razorpay.Client(auth=('rzp_test_9dZdkvIzTMtvp7', 'nEhr8fRsyi5vpATP774GOAUO'))

        # create order
        response_payment = client.order.create(dict(amount=amount, currency='INR')) 
        
        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created' :
            payment = Payment(
                name = name,
                email = email,
                amount = amount,
                order_id = order_id,
            )
            
            payment.save()       
            response_payment['name'] = name

            form = PaymentForm(request.POST or None)

            context={
                'form' : form,
                'payment' : response_payment,
                'order' : order,
                'cart_items'  :cart_items,
                'total' : total,
                'tax'  :tax,
                'grand_total' : grand_total,
            }
            return render(request,'payment.html', context)

    form = PaymentForm()
    return render(request,'payment.html',{'form':form ,'order':order})


@csrf_exempt
def payment_status(request) :
    response = request.POST
    params_dict ={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    
    #client instance
    client = razorpay.Client(auth=('rzp_test_9dZdkvIzTMtvp7', 'nEhr8fRsyi5vpATP774GOAUO'))
    
    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id']) 
        payment.razorpay_payment_id = response['razorpay_payment_id']
        payment.payment_method='razorpay'
        payment.paid = True 
        payment.save()

        tracking_no = request.session['tracking_no']
        order= Order.objects.get(tracking_no=tracking_no) 
        order.payment= payment
        order.is_ordered = True
        order.is_paid = True
        order.payment_method = 'razor pay'
        order.save()

        # move the cart item to orderproduct table
        cart_items=OrderItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = Myorder.objects.create(
            order_id = order.id,
            payment = payment,
            user_id = request.user.id,
            product_id = item.product_id,
            quantity = item.quantity,
            product_price = item.product.price,
            ordered = True,
            )
            order_product.save()
            
            # reduce the quantity of the sold products
            products = product.objects.get(id=item.product_id)
            products.stock -= item.quantity
            products.save()
        # clear cart
        OrderItem.objects.filter(user=request.user).delete()
        
      
        
        return render(request,'payment-status.html', {'status' : True})
    except :
        return render(request, 'payment-status.html', {'status' : False})
    
    
def cash_on_delivery(request) :
    if request.method == 'POST' :
        try :
            tracking_no = request.session['tracking_no']
            order= Order.objects.get(tracking_no=tracking_no) 
            order.is_ordered = True
            order.payment_method = 'Cash on Delivery'
            order.save()
            
            # move the cart item to orderproduct table
            cart_items=OrderItem.objects.filter(user=request.user)
            print(cart_items)

            for item in cart_items:
                order_product = Myorder.objects.create(
                order_id = order.id,
                user_id = request.user.id,
                product_id = item.product_id,
                quantity = item.quantity,
                product_price = item.product.price,
                ordered = True,
                )
                order_product.save()
                # reduce the quantity of the sold products
                products = product.objects.get(id=item.product_id)
                products.stock -= item.quantity
                products.save()
                
            # clear cart
            OrderItem.objects.filter(user=request.user).delete()
                
            return redirect('index')
        except :
            return redirect('cart')