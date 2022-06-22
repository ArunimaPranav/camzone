from types import ClassMethodDescriptorType
from django import forms
from django.forms import fields    
from . models import UserProfile,Address,Account
from  .import views



class RegistrationForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields=['first_name','last_name','email','mobile','gender','password']
        

    def __init__(self,*args,**kwargs):
        super(RegistrationForm ,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data    =super(RegistrationForm,self).clean()
        password        =cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
    
class UserForm(forms.ModelForm) :
    class Meta :
        model = Account
        fields = ['first_name', 'last_name', 'mobile']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            

class UserProfileForm(forms.ModelForm) :
    
    # To remove the text of current image in the form
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image Files Only")},widget=forms.FileInput)
    
    class Meta :
        model = UserProfile
        fields = ['address', 'city', 'state', 'country', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

################################### 
# class AddressForm(forms.ModelForm):
#     class Meta :
#         model = Address
#         fields = ['full_name', ' address', 'city', 'pin_code', 'state', 'country', 'mobile', 'landmark']
        

#     def _init_(self, *args, **kwargs):
#         super(AddressForm ,self)._init_(*args, **kwargs)

#         for field in self.fields :
#             self.fields[field].widget.attrs['class'] = 'form-control'