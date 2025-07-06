from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy, reverse
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
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION NUMBER {requisition.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {request.user.get_username()} ,\n\n'
                    f'Your requisition form has been successfully received. \n\n'
                    f'REQUISITION NUMBER : {requisition.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your requisition on the dashboard at the link: \n {dashboard_url} \n\n'
                    f'Regards, \n '
                    f'CCDO Team'
                ),
                to=[request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW REQUISITION NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new requisition number {requisition.ID} has been submitted by {request.user.get_username()} '
                    f'and is awaiting your review.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[finance.email],
            )
            finance_email.send(fail_silently=False)
                
            return redirect(self.success_url)
        
        return render(request, self.template_name, {
            'requisition_form' : requisition_form,
            'item_formset' : item_formset
        })
    
class VoucherView(LoginRequiredMixin, CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = "CashTracker/voucher.html"
    success_url = reverse_lazy("voucher")
    
class RetirementView(LoginRequiredMixin, TemplateView):
    model = Retirement
    template_name = "CashTracker/retirement.html"
    
class DownloadView(LoginRequiredMixin, TemplateView):
    # model = Retirement
    template_name = "CashTracker/download.html"