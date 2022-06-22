from django.shortcuts import redirect, render
from product.models import *
from product.forms import ProductForm

# Create your views here.
def add_product(request):
    if request.method=='POST':
       form=ProductForm(request.POST,request.FILES)
       if form.is_valid():
          form.save()
          
       return redirect('/')
    else:
        form=ProductForm()
    return render(request,'add_product.html', {'form':form})
def view_product(request,slug):
    
    products = product.objects.get(slug=slug)
    context = {"products": products}
    return render(request, "productdetails.html", context)

    