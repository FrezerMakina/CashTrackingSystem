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
        
        
ItemFormSet = modelformset_factory(Item, form=ItemForm, extra=1, can_delete=True)

    
class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['requisitionid', 'purpose', 'ID',]
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 2, 'cols': 30, 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        requisition_queryset = kwargs.pop('requisition_queryset', None)
        super().__init__(*args, **kwargs)
        if requisition_queryset is not None:
            self.fields['requisitionid'].queryset = requisition_queryset
        
class RetirementForm(forms.ModelForm):
    class Meta:
        model = Retirement
        fields = ['voucherid', 'requisitionid']
        
    def __init__(self, *args, **kwargs):
        voucher_queryset = kwargs.pop('voucher_queryset', None)
        super().__init__(*args, **kwargs)
        if voucher_queryset is not None:
            self.fields['voucherid'].queryset = voucher_queryset