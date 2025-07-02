from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import *

# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    
class DashboardView(LoginRequiredMixin, TemplateView):
    model = Staff
    template_name = "CashTracker/dashboard.html"
    
class RequisitionView(LoginRequiredMixin, TemplateView):
    # form_class = RequisitionForm
    # model = Requisition
    template_name = "CashTracker/requisition.html"
    success_url = reverse_lazy("requisition")
    
    def get(self, request, *args, **kwargs):
        return render( request, self.template_name, {
            'requisition_form' : RequisitionForm(),
            'item_formset' : ItemFormSet(queryset=Item.objects.none()),
        })
        
    def post(self, request, *args, **kwargs):
        requisition_form = RequisitionForm(request.POST)
        item_formset = ItemFormSet(request.POST)
        
        if requisition_form.is_valid() and item_formset.is_valid():
            requisition = requisition_form.save()
            items = item_formset.save(commit=False)
            
            for item in items:
                item.requisitionid = requisition
                item.save()
                
            return redirect(self.success_url)
        
        return render(request, self.template_name, {
            'requisition_form' : requisition_form,
            'item_formset' : item_formset
        })
    
class VoucherView(LoginRequiredMixin, TemplateView):
    model = Voucher
    template_name = "CashTracker/voucher.html"
    
class RetirementView(LoginRequiredMixin, TemplateView):
    model = Retirement
    template_name = "CashTracker/retirement.html"
    
class DownloadView(LoginRequiredMixin, TemplateView):
    # model = Retirement
    template_name = "CashTracker/download.html"