from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.db.models import Sum
from django.template.loader import render_to_string
from weasyprint import HTML
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from .models import *

# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    
# class DashboardView(LoginRequiredMixin, TemplateView):
#     model = Staff
#     template_name = "CashTracker/dashboard.html"
    
    
class DashboardView(LoginRequiredMixin, View):
    template_name = "CashTracker/dashboard.html"
    def get(self, request, *args, **kwargs):
        # vouchers = Voucher.objects.all()
        # requisitions = Requisition.objects.all() 
        # retirements = Retirement.objects.all()
        
        vouchersadmin = Voucher.objects.all()
        requisitionsadmin = Requisition.objects.all()
        retirementsadmin = Retirement.objects.all()
        
        vouchers = Voucher.objects.filter(createdby=request.user.get_username())
        requisitions = Requisition.objects.filter(createdby=request.user.get_username()) 
        retirements = Retirement.objects.filter(createdby=request.user.get_username())
        
        for requisition in requisitions:
            total_req = Item.objects.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            requisition.total = total_req
        
        for voucher in vouchers:
            total_voucher = Item.objects.filter(requisitionid=voucher.requisitionid).aggregate(total=Sum('totalprice'))['total'] or 0
            voucher.total = total_voucher
            
        for retirement in retirements:
            total_retirement = Item.objects.filter(requisitionid=retirement.requisitionid).aggregate(total=Sum('totalprice'))['total'] or 0
            retirement.total = total_retirement
 
            
        

        return render(request, self.template_name, {
            'vouchers' : vouchers,
            'requisitions' : requisitions,
            'retirements' : retirements,
            'vouchersadmin' : vouchersadmin,
            'requisitionsadmin' : requisitionsadmin,
            'retirementsadmin' : retirementsadmin,
        })
            

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
            requisition = requisition_form.save(commit=False)
            requisition.createdby = request.user.get_username()
            requisition.save()
            items = item_formset.save(commit=False)
            
            for item in items:
                item.requisitionid = requisition
                item.save()
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION NUMBER {requisition.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {request.user.get_username()} ,\n\n'
                    f'Your requisition form has been successfully received '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'REQUISITION NUMBER : {requisition.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your requisition on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
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
    
class VoucherView(LoginRequiredMixin, View):
    # model = Voucher
    # form_class = VoucherForm
    template_name = "CashTracker/voucher.html"
    # success_url = reverse_lazy("voucher")
    
    def get(self, request, *args, **kwargs):
                requisitions = Requisition.objects.filter(createdby=request.user.get_username(), status='Authorised')
                voucher_form = VoucherForm(requisition_queryset=requisitions)
            
                return render(request, self.template_name, {
                    'voucher_form' : voucher_form,
                    'requisitions' : requisitions,
                })

        
    def post(self, request, *args, **kwargs):
        voucher_form = VoucherForm(request.POST)
        requisitions = Requisition.objects.all()
        if voucher_form.is_valid():
            voucher = voucher_form.save(commit=False)
            voucher.createdby = request.user.get_username()
            voucher.save()
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'VOUCHER NUMBER {voucher.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {request.user.get_username()} ,\n\n'
                    f'Your voucher has been created successfully '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'VOUCHER NUMBER : {voucher.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your voucher on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW CASH VOUCHER NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new cash voucher number {voucher.ID} has been submitted by {request.user.get_username()} '
                    f'and is awaiting your review.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[finance.email],
            )
            finance_email.send(fail_silently=False)
                
            return redirect('voucher')
        
        return render(request, self.template_name, {
            'voucher_form' : voucher_form,
            'requisitions': requisitions,
        })
        
    
class VoucherajaxView(LoginRequiredMixin, View):
    def get(self, request, requisitionid, *args, **kwargs):
        try:
            requisition = Requisition.objects.get(pk=requisitionid, createdby=request.user.get_username(), status='Authorised')
            department = requisition.requestingdept
            total_amount = Item.objects.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            
            return JsonResponse({
                'department' : department,
                'amount' : float(total_amount),
            })
            
        except Requisition.DoesNotExist:
            return JsonResponse({'error' : 'Requistion not found'}, status=404)



class RetirementView(LoginRequiredMixin, View):
    # model = Voucher
    # form_class = VoucherForm
    template_name = "CashTracker/retirement.html"
    # success_url = reverse_lazy("voucher")
    
    def get(self, request, *args, **kwargs):
                vouchers = Voucher.objects.filter(createdby=request.user.get_username(), status='Authorised')
                retirement_form = RetirementForm(voucher_queryset=vouchers)
            
                return render(request, self.template_name, {
                    'retirement_form' : retirement_form,
                    'vouchers' : vouchers,
                })

        
    def post(self, request, *args, **kwargs):
        retirement_form = RetirementForm(request.POST)
        vouchers = Voucher.objects.all()
        if retirement_form.is_valid():
            retirement = retirement_form.save(commit=False)
            retirement.createdby = request.user.get_username()
            retirement.save()
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'RETIREMENT FORM NUMBER {retirement.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {request.user.get_username()} ,\n\n'
                    f'Your retirement form has been created successfully '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'RETIREMENT FORM NUMBER : {retirement.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your retirement form on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW CASH RETIREMENT FORM NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new cash retirement form number {retirement.ID} has been submitted by {request.user.get_username()} '
                    f'and is awaiting your review.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[finance.email],
            )
            finance_email.send(fail_silently=False)
                
            return redirect('retirement')
        
        return render(request, self.template_name, {
            'retirement_form' : retirement_form,
            'vouchers': vouchers,
        })
    
    
    
class RetirementajaxView(LoginRequiredMixin, View):
    def get(self, request, voucherid, *args, **kwargs):
        try:
            voucher = Voucher.objects.get(pk=voucherid, createdby=request.user.get_username(), status='Authorised')
            requisition = voucher.requisitionid            
            items = Item.objects.filter(requisitionid=requisition)
            total_amount = items.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            
            
            item_list = []
            for item in items:
                item_list.append({
                    'itemname' : item.itemname,
                    'totalprice' : item.totalprice, 
                    'unitprice' : item.unitprice,
                    'quantity' : item.quantity,  
                })
            
            
            return JsonResponse({
                'requisitionid' : requisition.pk,
                'amount' : float(total_amount),
                'item_list' : item_list,
            })
            
        except Voucher.DoesNotExist:
            return JsonResponse({'error' : 'Voucher not found'}, status=404)  
        
        except Requisition.DoesNotExist:
            return JsonResponse({'error' : 'Requisition not found'}, status=404)  

    
    
    
class ItemsajaxView(LoginRequiredMixin, View):
    def get(self, request, requisitionid, *args, **kwargs):
        try:
            requisition = Requisition.objects.get(pk=requisitionid)           
            items = Item.objects.filter(requisitionid=requisition)
            total_amount = items.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            
            
            item_list = []
            for item in items:
                item_list.append({
                    'itemname' : item.itemname,
                    'totalprice' : item.totalprice, 
                    'unitprice' : item.unitprice,
                    'quantity' : item.quantity,
                    'reason' : item.reason,  
                })
            
            
            return JsonResponse({
                'requisitionid' : requisition.pk,
                'amount' : float(total_amount),
                'item_list' : item_list,
            })
            
        except Requisition.DoesNotExist:
            return JsonResponse({'error' : 'Requisition not found'}, status=404) 
    
    

    
class RequisitionUpdateView(LoginRequiredMixin, UpdateView):
    model = Requisition
    form_class = RequisitionForm
    template_name = 'CashTracker/updates/requisition.html'
    success_url = reverse_lazy('requisition')
    
    def form_valid(self, form):
        requisition = form.save(commit=False)
        if self.request.user.role == "Finance Officer":
            requisition.status = "Reviewed"
            requisition.save()
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION FORM NUMBER {requisition.ID} REVIEWED',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'You have successfully reviewed the requisition form of {requisition.createdby}'
                    f' and it has been sent to the PROGRAMS MANAGER OFFICE for approval\n\n'
                    f'REQUISITION FORM NUMBER : {requisition.ID} \n\n'
                    f'Thank you for your review\n'
                    f'You can check on the dashboard if there are other forms needing your attention on the the link below: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            programs = Staff.objects.filter(role='Programs Manager').first()
            programs_email = EmailMessage(
                subject=f'NEW CASH REQUISTION FORM NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {programs.username} ,\n\n'
                    f'A new cash requisition form number {requisition.ID} submitted by {requisition.createdby} has been reviewed by {self.request.user.get_username()} '
                    f'and is awaiting your approval.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[programs.email],
            )
            programs_email.send(fail_silently=False)
            
            
            
            
            reqowner = Staff.objects.filter(username=requisition.createdby).first()
            reqowner_email = EmailMessage(
                subject=f'CASH REQUISTION FORM NUMBER {requisition.ID} REVIEWED',
                body=(
                    f'Hello {reqowner.username} ,\n\n'
                    f'Your cash requisition form number {requisition.ID} has been reviewed at the FINANCES OFFICE and is at the PROGRAMS MANAGER\'S OFFICE awaiting approval\n\n'
                    f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[reqowner.email],
            )
            reqowner_email.send(fail_silently=False)
            
            return super().form_valid(form)
        
        
        elif self.request.user.role == "Programs Manager":
            requisition.status = "Approved"
            requisition.save()
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION FORM NUMBER {requisition.ID} APPROVED',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'You have successfully approved the requisition form of {requisition.createdby}'
                    f' and it has been sent to the EXECUTIVE DIRECTOR\'S OFFICE for authorisation\n\n'
                    f'REQUISITION FORM NUMBER : {requisition.ID} \n\n'
                    f'Thank you for your approval\n'
                    f'You can check on the dashboard if there are other forms needing your attention on the the link below: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            ed = Staff.objects.filter(role='ED').first()
            ed_email = EmailMessage(
                subject=f'NEW CASH REQUISTION FORM NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {ed.username} ,\n\n'
                    f'A new cash requisition form number {requisition.ID} submitted by {requisition.createdby} has been approved by {self.request.user.get_username()} '
                    f'and is awaiting your authorisation.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[ed.email],
            )
            ed_email.send(fail_silently=False)
            
            
            
            
            reqowner = Staff.objects.filter(username=requisition.createdby).first()
            reqowner_email = EmailMessage(
                subject=f'CASH REQUISTION FORM NUMBER {requisition.ID} APPROVED',
                body=(
                    f'Hello {reqowner.username} ,\n\n'
                    f'Your cash requisition form number {requisition.ID} has been approved at the PROGRAMS MANAGER OFFICE\'S OFFICE and is at the EXECUTIVE DIRECTOR\'S OFFICE awaiting authorisation\n\n'
                    f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[reqowner.email],
            )
            reqowner_email.send(fail_silently=False)
            
            return super().form_valid(form)
        
        
        elif self.request.user.role == "ED":
            requisition.status = "Authorised"
            requisition.save()
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION FORM NUMBER {requisition.ID} AUTHORISED',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'You have successfully authorised the requisition form of {requisition.createdby}'
                    f' and an email has been also sent to {requisition.createdby} so that a voucher can be created\n\n'
                    f'REQUISITION FORM NUMBER : {requisition.ID} \n\n'
                    f'Thank you for your authorisation\n'
                    f'You can check on the dashboard if there are other forms needing your attention on the the link below: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            
            reqowner = Staff.objects.filter(username=requisition.createdby).first()
            reqowner_email = EmailMessage(
                subject=f'CASH REQUISTION FORM NUMBER {requisition.ID} APPROVED',
                body=(
                    f'Hello {reqowner.username} ,\n\n'
                    f'Your cash requisition form number {requisition.ID} has been authorised at the EXECUTIVE DIRECTOR\'S OFFICE\n\n'
                    f'Log into the Cash Tracking system and create the voucher for this authorised requisition\n\n'
                    f'You can be checking for the status of other forms by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[reqowner.email],
            )
            reqowner_email.send(fail_silently=False)
            
            return super().form_valid(form)
        
        
class DownloadView(LoginRequiredMixin, TemplateView):
    template_name = "CashTracker/download.html"
    def get(self, request, *args, **kwargs):
       
        vouchers = Voucher.objects.filter(status='Authorised')
        requisitions = Requisition.objects.filter(status='Authorised') 
        retirements = Retirement.objects.filter(status='Authorised')
        
        for requisition in requisitions:
            total_req = Item.objects.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            requisition.total = total_req
        
        for voucher in vouchers:
            total_voucher = Item.objects.filter(requisitionid=voucher.requisitionid).aggregate(total=Sum('totalprice'))['total'] or 0
            voucher.total = total_voucher
            
        for retirement in retirements:
            total_retirement = Item.objects.filter(requisitionid=retirement.requisitionid).aggregate(total=Sum('totalprice'))['total'] or 0
            retirement.total = total_retirement
 
            
        

        return render(request, self.template_name, {
            'vouchers' : vouchers,
            'requisitions' : requisitions,
            'retirements' : retirements,
          
        })
    
    
class RequisitionDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        requisition = Requisition.objects.get(pk=pk)
        items = Item.objects.filter(requisitionid=requisition)
        total_amount = items.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
        html_string = render_to_string('CashTracker/pdf/requisition_pdf.html', {
            'requisition' : requisition,
            'items' : items,
            'total_amount' : total_amount,
        })
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="requisition_{requisition.ID}.pdf"'
        return response