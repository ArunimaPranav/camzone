
from django import forms
from product.models import *




class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ("category", "name", "img","img1","img2", "desc", "price", "stock")
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"