from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = ('username', 'email', 'role', 'password1', 'password2')
        
class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['activityname', 'projectname', 'projectcode', 'requestingdept', 'ID' ]
        
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemname', 'reason', 'quantity', 'unitprice', 'totalprice']
        
        
ItemFormSet = modelformset_factory(Item, form=ItemForm, extra=4, can_delete=True)

    
class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['purpose',]
        
        
class RetirementForm(forms.ModelForm):
    class Meta:
        model = Retirement
        fields = []