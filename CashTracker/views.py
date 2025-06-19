from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
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
    model = Requisition
    template_name = "CashTracker/requisition.html"
    
class VoucherView(LoginRequiredMixin, TemplateView):
    model = Voucher
    template_name = "CashTracker/voucher.html"
    
class RetirementView(LoginRequiredMixin, TemplateView):
    model = Retirement
    template_name = "CashTracker/retirement.html"
    
class DownloadView(LoginRequiredMixin, TemplateView):
    # model = Retirement
    template_name = "CashTracker/download.html"