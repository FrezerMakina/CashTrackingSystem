from django.shortcuts import render, redirect
from django.contrib import messages
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
        req_completed = Requisition.objects.filter(status__in=['Authorised', 'Done'], createdby=request.user.get_username()).count()
        voucher_completed = Voucher.objects.filter(status__in=['Authorised', 'Done'], createdby=request.user.get_username()).count()
        ret_completed = Retirement.objects.filter(status__in=['Authorised', 'Done'], createdby=request.user.get_username()).count()
        completed_count = req_completed + voucher_completed + ret_completed
        
        user_req_back = Requisition.objects.filter(status__in=['Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED'], createdby=request.user.get_username()).count()
        user_voucher_back = Voucher.objects.filter(status__in=['Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED'], createdby=request.user.get_username()).count()
        user_ret_back = Retirement.objects.filter(status__in=['Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED'], createdby=request.user.get_username()).count()
        user_back_count = user_req_back + user_voucher_back + user_ret_back
        
        user_req_rej = Requisition.objects.filter(status__in=['Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED'], createdby=request.user.get_username()).count()
        user_voucher_rej = Voucher.objects.filter(status__in=['Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED'], createdby=request.user.get_username()).count()
        user_ret_rej = Retirement.objects.filter(status__in=['Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED'], createdby=request.user.get_username()).count()
        user_rej_count = user_req_rej + user_voucher_rej + user_ret_rej
        
        user_req_process = Requisition.objects.filter(createdby=self.request.user.get_username()).exclude(status__in=['Authorised', 'Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED', 'Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED', 'Done']).count()
        user_voucher_process = Voucher.objects.filter(createdby=self.request.user.get_username()).exclude(status__in=['Authorised', 'Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED', 'Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED', 'Done']).count()
        user_ret_process = Retirement.objects.filter(createdby=self.request.user.get_username()).exclude(status__in=['Authorised', 'Sent Back by Finance Officer', 'Sent Back by Programs Manager', 'Sent Back by ED', 'Rejected by Finance Officer', 'Rejected by Programs Manager', 'Rejected by ED', 'Done']).count()
        user_process_count = user_req_process + user_voucher_process + user_ret_process
        
        req_submitted = Requisition.objects.filter(status="SUBMIITED").count()
        voucher_submitted = Voucher.objects.filter(status="SUBMITTED").count()
        ret_submitted = Retirement.objects.filter(status="SUBMITTED").count()
        submitted_count = req_submitted + voucher_submitted + ret_submitted
        
        req_reviewed = Requisition.objects.filter(status="Reviewed").count()
        voucher_reviewed = Voucher.objects.filter(status="Reviewed").count()
        ret_reviewed = Retirement.objects.filter(status="Reviewed").count()
        reviewed_count = req_reviewed + voucher_reviewed + ret_reviewed
        
        req_approved = Requisition.objects.filter(status="Approved").count()
        voucher_approved = Voucher.objects.filter(status="Approved").count()
        ret_approved = Retirement.objects.filter(status="Approved").count()
        approved_count = req_approved + voucher_approved + ret_approved
        
        req_authorised = Requisition.objects.filter(status__in=['Authorised', 'Done']).count()
        voucher_authorised = Voucher.objects.filter(status__in=['Authorised', 'Done']).count()
        ret_authorised = Retirement.objects.filter(status__in=['Authorised', 'Done']).count()
        authorised_count = req_authorised + voucher_authorised + ret_authorised
        
        req_back_fin = Requisition.objects.filter(status="Sent Back by Finance Officer").count()
        voucher_back_fin = Voucher.objects.filter(status="Sent Back by Finance Officer").count()
        ret_back_fin = Retirement.objects.filter(status="Sent Back by Finance Officer").count()
        back_fin_count = req_back_fin + voucher_back_fin + ret_back_fin
        
        req_back_programs = Requisition.objects.filter(status="Sent Back by Programs Manager").count()
        voucher_back_programs = Voucher.objects.filter(status="Sent Back by Programs Manager").count()
        ret_back_programs = Retirement.objects.filter(status="Sent Back by Programs Manager").count()
        back_programs_count = req_back_programs + voucher_back_programs + ret_back_programs
        
        req_back_ed = Requisition.objects.filter(status="Sent Back by ED").count()
        voucher_back_ed = Voucher.objects.filter(status="Sent Back by ED").count()
        ret_back_ed = Retirement.objects.filter(status="Sent Back by ED").count()
        back_ed_count = req_back_ed + voucher_back_ed + ret_back_ed
        
        req_rej_fin = Requisition.objects.filter(status="Rejected by Finance Officer").count()
        voucher_rej_fin = Voucher.objects.filter(status="Rejected by Finance Officer").count()
        ret_rej_fin = Retirement.objects.filter(status="Rejected by Finance Officer").count()
        rej_fin_count = req_rej_fin + voucher_rej_fin + ret_rej_fin
        
        req_rej_programs = Requisition.objects.filter(status="Rejected by Programs Manager").count()
        voucher_rej_programs = Voucher.objects.filter(status="Rejected by Programs Manager").count()
        ret_rej_programs = Retirement.objects.filter(status="Rejected by Programs Manager").count()
        rej_programs_count = req_rej_programs + voucher_rej_programs + ret_rej_programs
        
        req_rej_ed = Requisition.objects.filter(status="Rejected by ED").count()
        voucher_rej_ed = Voucher.objects.filter(status="Rejected by ED").count()
        ret_rej_ed = Retirement.objects.filter(status="Rejected by ED").count()
        rej_ed_count = req_rej_ed + voucher_rej_ed + ret_rej_ed
        # vouchers = Voucher.objects.all()
        # requisitions = Requisition.objects.all() 
        # retirements = Retirement.objects.all()
        
        vouchersadmin = Voucher.objects.all()
        requisitionsadmin = Requisition.objects.all()
        retirementsadmin = Retirement.objects.all()
        
        vouchers = Voucher.objects.filter(createdby=self.request.user.get_username())
        requisitions = Requisition.objects.filter(createdby=self.request.user.get_username()) 
        retirements = Retirement.objects.filter(createdby=self.request.user.get_username())
        
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
            'reviewed_count' : reviewed_count,
            'approved_count' : approved_count,
            'authorised_count' : authorised_count,
            'back_fin_count' : back_fin_count,
            'back_programs_count' : back_programs_count,
            'back_ed_count' : back_ed_count,
            'rej_fin_count' : rej_fin_count,
            'rej_programs_count' : rej_programs_count,
            'rej_ed_count' : rej_ed_count,
            'submitted_count' : submitted_count,
            'completed_count' : completed_count,
            'user_back_count' : user_back_count,
            'user_rej_count' : user_rej_count,
            'user_process_count' : user_process_count,
        })
            

class RequisitionView(LoginRequiredMixin, TemplateView):
    # form_class = RequisitionForm
    # model = Requisition
    template_name = "CashTracker/requisition.html"
    success_url = reverse_lazy("dashboard")
    
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
            requisition.createdby = self.request.user.get_username()
            requisition.save()
            messages.success(self.request, f"Requisition REQ-00{requisition.ID} saved successfully.")
            items = item_formset.save(commit=False)
            
            for item in items:
                item.requisitionid = requisition
                item.save()
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'REQUISITION NUMBER REQ-00{requisition.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'Your requisition form has been successfully received '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'REQUISITION NUMBER : REQ-00{requisition.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your requisition on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW REQUISITION NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new requisition number REQ-00{requisition.ID} has been submitted by {self.request.user.get_username()} '
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
    # success_url = reverse_lazy("dashboard")
    
    def get(self, request, *args, **kwargs):
                requisitions = Requisition.objects.filter(createdby=self.request.user.get_username(), status='Authorised')
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
            voucher.createdby = self.request.user.get_username()
            voucher.save()
            
            requisition = voucher.requisitionid  
            requisition.status = 'Done'
            requisition.save()
            
            messages.success(self.request, f"Voucher PV-00{voucher.ID} saved successfully.")
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'VOUCHER NUMBER PV-00{voucher.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'Your voucher has been created successfully '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'VOUCHER NUMBER : PV-00{voucher.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your voucher on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW CASH VOUCHER NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new cash voucher number PV-00{voucher.ID} has been submitted by {self.request.user.get_username()} '
                    f'and is awaiting your review.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[finance.email],
            )
            finance_email.send(fail_silently=False)
                
            return redirect('dashboard')
        
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
        retirement_form = RetirementForm(request.POST, request.FILES)
        vouchers = Voucher.objects.all()
        if retirement_form.is_valid():
            retirement = retirement_form.save(commit=False)
            retirement.createdby = self.request.user.get_username()
            retirement.save()
            
            voucher = retirement.voucherid  
            voucher.status = 'Done'
            voucher.save()
            
            messages.success(self.request, f"Retirement CR-00{retirement.ID} saved successfully.")
               
            dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
            user_email = EmailMessage(
                subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} SUBMITTED SUCCESSFULLY',
                body=(
                    f'Hello {self.request.user.get_username()} ,\n\n'
                    f'Your retirement form has been created successfully '
                    f'and it is now at FINANCE OFFICE for review\n\n'
                    f'RETIREMENT FORM NUMBER : CR-00{retirement.ID} \n\n'
                    f'You will be notified of next steps in due course. \n \n'
                    f'You can be checking for the status of your retirement form on the dashboard at the link: \n{dashboard_url} \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[self.request.user.email],
            )
            user_email.send(fail_silently=False)
            
            finance = Staff.objects.filter(role='Finance Officer').first()
            finance_email = EmailMessage(
                subject=f'NEW CASH RETIREMENT FORM NEEDING YOUR ATTENTION',
                body=(
                    f'Hello {finance.username} ,\n\n'
                    f'A new cash retirement form number CR-00{retirement.ID} has been submitted by {self.request.user.get_username()} '
                    f'and is awaiting your review.\n\n'
                    f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                    f'Your timely review and feedback will be key in this process \n\n'
                    f'Regards, \n'
                    f'CCDO Team'
                ),
                to=[finance.email],
            )
            finance_email.send(fail_silently=False)
                
            return redirect('dashboard')
        
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
                'dept' : requisition.requestingdept,
                'requisitionid' : requisition.pk,
                'amount' : float(total_amount),
                'item_list' : item_list,
            })
            
        except Requisition.DoesNotExist:
            return JsonResponse({'error' : 'Requisition not found'}, status=404) 
    
    

    
class RequisitionReviewView(LoginRequiredMixin, UpdateView):
    model = Requisition
    form_class = RequisitionForm
    template_name = 'CashTracker/review/requisition_review.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        requisition = form.save(commit=False)
        action = self.request.POST.get("action")
        comments = self.request.POST.get("comments", "").strip()
        dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
        
        if action == "reject":
            requisition.status = f'Rejected by {self.request.user.role}'
            requisition.save()
            messages.success(self.request, f"Requisition REQ-00{requisition.ID} rejected successfully.")

        # Notify requester
            requester = Staff.objects.filter(username=requisition.createdby).first()
            EmailMessage(
                subject=f'REQUISITION FORM NUMBER REQ-00{requisition.ID} REJECTED',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your requisition form number REQ-00{requisition.ID} has been rejected by {self.request.user.get_username()}\n\n'
                    f'COMMENTS: {comments if comments else "No additional comments."}\n\n'
                    f'You can chech on the dashboard for the status of other forms: {dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)

            return super().form_valid(form)
        
        elif action == "send_back":
            requisition.status = f'Sent Back by {self.request.user.role}'
            requisition.save()
            messages.success(self.request, f"Requisition REQ-00{requisition.ID} sent back successfully.")

            # Notify requester
            requester = Staff.objects.filter(username=requisition.createdby).first()
            EmailMessage(
                subject=f'REQUISITION FORM NUMBER REQ-00{requisition.ID} SENT BACK FOR CORRECTION',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your requisition form number REQ-00{requisition.ID} has been sent back for correction by {self.request.user.get_username()}.\n\n'
                    f'Comment: {comments if comments else "No additional comments."}\n\n'
                    f'Please log in to submit a new requesition based on the comments provides.\n\nYou can also check for the status of other forms on the link: \n{dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)
            return super().form_valid(form)
        
        elif action == "accept":
            if self.request.user.role == "Finance Officer":
                requisition.status = "Reviewed"
                requisition.save()
                messages.success(self.request, f"Requisition REQ-00{requisition.ID} reviewed successfully.")
            
                user_email = EmailMessage(
                    subject=f'REQUISITION FORM NUMBER REQ-00{requisition.ID} REVIEWED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully reviewed the requisition form of {requisition.createdby}'
                        f' and it has been sent to the PROGRAMS MANAGER OFFICE for approval\n\n'
                        f'REQUISITION FORM NUMBER : REQ-00{requisition.ID} \n\n'
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
                        f'A new cash requisition form number REQ-00{requisition.ID} submitted by {requisition.createdby} has been reviewed by {self.request.user.get_username()} '
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
                    subject=f'CASH REQUISTION FORM NUMBER REQ-00{requisition.ID} REVIEWED',
                    body=(
                        f'Hello {reqowner.username} ,\n\n'
                        f'Your cash requisition form number REQ-00{requisition.ID} has been reviewed at the FINANCES OFFICE and is at the PROGRAMS MANAGER\'S OFFICE awaiting approval\n\n'
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
                messages.success(self.request, f"Requisition REQ-00{requisition.ID} approved successfully.")
            
                user_email = EmailMessage(
                    subject=f'REQUISITION FORM NUMBER REQ-00{requisition.ID} APPROVED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully approved the requisition form of {requisition.createdby}'
                        f' and it has been sent to the EXECUTIVE DIRECTOR\'S OFFICE for authorisation\n\n'
                        f'REQUISITION FORM NUMBER : REQ-00{requisition.ID} \n\n'
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
                        f'A new cash requisition form number REQ-00{requisition.ID} submitted by {requisition.createdby} has been approved by {self.request.user.get_username()} '
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
                    subject=f'CASH REQUISTION FORM NUMBER REQ-00{requisition.ID} APPROVED',
                    body=(
                        f'Hello {reqowner.username} ,\n\n'
                        f'Your cash requisition form number REQ-00{requisition.ID} has been approved at the PROGRAMS MANAGER OFFICE\'S OFFICE and is at the EXECUTIVE DIRECTOR\'S OFFICE awaiting authorisation\n\n'
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
                messages.success(self.request, f"Requisition REQ-00{requisition.ID} authorised successfully.")
             
                user_email = EmailMessage(
                    subject=f'REQUISITION FORM NUMBER REQ-00{requisition.ID} AUTHORISED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully authorised the requisition form of {requisition.createdby}'
                        f' and an email has been also sent to {requisition.createdby} so that a voucher can be created\n\n'
                        f'REQUISITION FORM NUMBER : REQ-00{requisition.ID} \n\n'
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
                    subject=f'CASH REQUISTION FORM NUMBER REQ-00{requisition.ID} APPROVED',
                    body=(
                        f'Hello {reqowner.username} ,\n\n'
                        f'Your cash requisition form number REQ-00{requisition.ID} has been authorised at the EXECUTIVE DIRECTOR\'S OFFICE\n\n'
                        f'Log into the Cash Tracking system and create the voucher for this authorised requisition\n\n'
                        f'You can be checking for the status of other forms by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[reqowner.email],
                )
                reqowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
        
class VoucherReviewView(LoginRequiredMixin, UpdateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'CashTracker/review/voucher_review.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        voucher = form.save(commit=False)
        action = self.request.POST.get("action")
        comments = self.request.POST.get("comments", "").strip()
        dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
        
        if action == "reject":
            voucher.status = f'Rejected by {self.request.user.role}'
            voucher.save()
            messages.success(self.request, f"Voucher PV-00{voucher.ID} rejected successfully.")

        # Notify requester
            requester = Staff.objects.filter(username=voucher.createdby).first()
            EmailMessage(
                subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} REJECTED',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your voucher form number PV-00{voucher.ID} has been rejected by {self.request.user.get_username()}\n\n'
                    f'COMMENTS: {comments if comments else "No additional comments."}\n\n'
                    f'You can chech on the dashboard for the status of other forms: {dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)

            return super().form_valid(form)
        
        elif action == "send_back":
            voucher.status = f'Sent Back by {self.request.user.role}'
            voucher.save()
            messages.success(self.request, f"Voucher PV-00{voucher.ID} sent back successfully.")

            # Notify requester
            requester = Staff.objects.filter(username=voucher.createdby).first()
            EmailMessage(
                subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} SENT BACK FOR CORRECTION',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your voucher form number PV-00{voucher.ID} has been sent back for correction by {self.request.user.get_username()}.\n\n'
                    f'Comment: {comments if comments else "No additional comments."}\n\n'
                    f'Please log in to submit a new voucher based on the comments provides.\n\nYou can also check for the status of other forms on the link: \n{dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)
            return super().form_valid(form)
        
        elif action == "accept":
            if self.request.user.role == "Finance Officer":
                voucher.status = "Reviewed"
                voucher.save()
                messages.success(self.request, f"Voucher PV-00{voucher.ID} reviewed successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} REVIEWED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully reviewed the voucher form of {voucher.createdby}'
                        f' and it has been sent to the PROGRAMS MANAGER OFFICE for approval\n\n'
                        f'VOUCHER FORM NUMBER : PV-00{voucher.ID} \n\n'
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
                    subject=f'NEW VOUCHER FORM NEEDING YOUR ATTENTION',
                    body=(
                        f'Hello {programs.username} ,\n\n'
                        f'A new voucher form number PV-00{voucher.ID} submitted by {voucher.createdby} has been reviewed by {self.request.user.get_username()} '
                        f'and is awaiting your approval.\n\n'
                        f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Your timely review and feedback will be key in this process \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[programs.email],
                )
                programs_email.send(fail_silently=False)
            
            
            
            
                voucherowner = Staff.objects.filter(username=voucher.createdby).first()
                voucherowner_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} REVIEWED',
                    body=(
                        f'Hello {voucherowner.username} ,\n\n'
                        f'Your VOUCHER form number PV-00{voucher.ID} has been reviewed at the FINANCES OFFICE and is at the PROGRAMS MANAGER\'S OFFICE awaiting approval\n\n'
                        f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[voucherowner.email],
                )
                voucherowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
            elif self.request.user.role == "Programs Manager":
                voucher.status = "Approved"
                voucher.save()
                messages.success(self.request, f"Voucher PV-00{voucher.ID} approved successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} APPROVED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully approved the voucher form of {voucher.createdby}'
                        f' and it has been sent to the EXECUTIVE DIRECTOR\'S OFFICE for authorisation\n\n'
                        f'VOUCHER FORM NUMBER : PV-00{voucher.ID} \n\n'
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
                    subject=f'NEW VOUCHER FORM NEEDING YOUR ATTENTION',
                    body=(
                        f'Hello {ed.username} ,\n\n'
                        f'A new voucher form number PV-00{voucher.ID} submitted by {voucher.createdby} has been approved by {self.request.user.get_username()} '
                        f'and is awaiting your authorisation.\n\n'
                        f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Your timely review and feedback will be key in this process \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[ed.email],
                )
                ed_email.send(fail_silently=False)
            
            
            
            
                voucherowner = Staff.objects.filter(username=voucher.createdby).first()
                voucherowner_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} APPROVED',
                    body=(
                        f'Hello {voucherowner.username} ,\n\n'
                        f'Your voucher form number PV-00{voucher.ID} has been approved at the PROGRAMS MANAGER\'S OFFICE and is at the EXECUTIVE DIRECTOR\'S OFFICE awaiting authorisation\n\n'
                        f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[voucherowner.email],
                )
                voucherowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
            elif self.request.user.role == "ED":
                voucher.status = "Authorised"
                voucher.save()
                messages.success(self.request, f"Voucher PV-00{voucher.ID} authorised successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} AUTHORISED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully authorised the voucher form of {voucher.createdby}'
                        f' and an email has been also sent to {voucher.createdby} so that cash can be taken from accounts office\n\n'
                        f'VOUCHER FORM NUMBER : PV-00{voucher.ID} \n\n'
                        f'Thank you for your authorisation\n'
                        f'You can check on the dashboard if there are other forms needing your attention on the the link below: \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[self.request.user.email],
                )
                user_email.send(fail_silently=False)
            
            
                voucherowner = Staff.objects.filter(username=voucher.createdby).first()
                voucherowner_email = EmailMessage(
                    subject=f'VOUCHER FORM NUMBER PV-00{voucher.ID} APPROVED',
                    body=(
                        f'Hello {voucherowner.username} ,\n\n'
                        f'Your voucher form number PV-00{voucher.ID} has been authorised at the EXECUTIVE DIRECTOR\'S OFFICE\n\n'
                        f'Go to the accounts office and get the money for this voucher\n\n'
                        f'You can be checking for the status of other forms by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[voucherowner.email],
                )
                voucherowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
class RetirementReviewView(LoginRequiredMixin, UpdateView):
    model = Retirement
    form_class = RetirementForm
    template_name = 'CashTracker/review/retirement_review.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        retirement = form.save(commit=False)
        action = self.request.POST.get("action")
        comments = self.request.POST.get("comments", "").strip()
        dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
        
        if action == "reject":
            retirement.status = f'Rejected by {self.request.user.role}'
            retirement.save()
            messages.success(self.request, f"Retirement CR-00{retirement.ID} rejected successfully.")
            

        # Notify requester
            requester = Staff.objects.filter(username=retirement.createdby).first()
            EmailMessage(
                subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} REJECTED',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your retirement form number CR-00{retirement.ID} has been rejected by {self.request.user.get_username()}\n\n'
                    f'COMMENTS: {comments if comments else "No additional comments."}\n\n'
                    f'You can chech on the dashboard for the status of other forms: {dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)

            return super().form_valid(form)
        
        elif action == "send_back":
            retirement.status = f'Sent Back by {self.request.user.role}'
            retirement.save()
            messages.success(self.request, f"Retirement CR-00{retirement.ID} sent back successfully.")

            # Notify requester
            requester = Staff.objects.filter(username=retirement.createdby).first()
            EmailMessage(
                subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} SENT BACK FOR CORRECTION',
                body=(
                    f'Dear {requester.username},\n\n'
                    f'Your retirement form number CR-00{retirement.ID} has been sent back for correction by {self.request.user.get_username()}.\n\n'
                    f'Comment: {comments if comments else "No additional comments."}\n\n'
                    f'Please log in to submit a new retirement based on the comments provides.\n\nYou can also check for the status of other forms on the link: \n{dashboard_url}\n\n'
                    f'Regards,\nCCDO Team'
                ),
                to=[requester.email],
            ).send(fail_silently=False)
            return super().form_valid(form)
        
        elif action == "accept":
            if self.request.user.role == "Finance Officer":
                retirement.status = "Reviewed"
                retirement.save()
                messages.success(self.request, f"Retirement CR-00{retirement.ID} reviewed successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} REVIEWED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully reviewed the retirement form of {retirement.createdby}'
                        f' and it has been sent to the PROGRAMS MANAGER OFFICE for approval\n\n'
                        f'VOUCHER FORM NUMBER : CR-00{retirement.ID} \n\n'
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
                    subject=f'NEW RETIREMENT FORM NEEDING YOUR ATTENTION',
                    body=(
                        f'Hello {programs.username} ,\n\n'
                        f'A new retirement form number CR-00{retirement.ID} submitted by {retirement.createdby} has been reviewed by {self.request.user.get_username()} '
                        f'and is awaiting your approval.\n\n'
                        f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Your timely review and feedback will be key in this process \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[programs.email],
                )
                programs_email.send(fail_silently=False)
            
            
            
            
                retirementowner = Staff.objects.filter(username=retirement.createdby).first()
                retirementowner_email = EmailMessage(
                    subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} REVIEWED',
                    body=(
                        f'Hello {retirementowner.username} ,\n\n'
                        f'Your RETIREMENT form number CR-00{retirement.ID} has been reviewed at the FINANCES OFFICE and is at the PROGRAMS MANAGER\'S OFFICE awaiting approval\n\n'
                        f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[retirementowner.email],
                )
                retirementowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
            elif self.request.user.role == "Programs Manager":
                retirement.status = "Approved"
                retirement.save()
                messages.success(self.request, f"Retirement CR-00{retirement.ID} approved successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} APPROVED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully approved the retirement form of {retirement.createdby}'
                        f' and it has been sent to the EXECUTIVE DIRECTOR\'S OFFICE for authorisation\n\n'
                        f'RETIREMENT FORM NUMBER : CR-00{retirement.ID} \n\n'
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
                    subject=f'NEW RETIREMENT FORM NEEDING YOUR ATTENTION',
                    body=(
                        f'Hello {ed.username} ,\n\n'
                        f'A new retirement form number CR-00{retirement.ID} submitted by {retirement.createdby} has been approved by {self.request.user.get_username()} '
                        f'and is awaiting your authorisation.\n\n'
                        f'Please review it by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Your timely review and feedback will be key in this process \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[ed.email],
                )
                ed_email.send(fail_silently=False)
            
            
            
            
                retirementowner = Staff.objects.filter(username=retirement.createdby).first()
                retirementowner_email = EmailMessage(
                    subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} APPROVED',
                    body=(
                        f'Hello {retirementowner.username} ,\n\n'
                        f'Your retirement form number CR-00{retirement.ID} has been approved at the PROGRAMS MANAGER OFFICE\'S OFFICE and is at the EXECUTIVE DIRECTOR\'S OFFICE awaiting authorisation\n\n'
                        f'You can be checking for it\'s status by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[retirementowner.email],
                )
                retirementowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
            elif self.request.user.role == "ED":
                retirement.status = "Authorised"
                retirement.save()
                messages.success(self.request, f"Retirement CR-00{retirement.ID} authorised successfully.")
                dashboard_url = self.request.build_absolute_uri(reverse('dashboard')) 
                user_email = EmailMessage(
                    subject=f'RETIREMENT FORM NUMBER CR-00{retirement.ID} AUTHORISED',
                    body=(
                        f'Hello {self.request.user.get_username()} ,\n\n'
                        f'You have successfully authorised the retirement form of {retirement.createdby}'
                        f' and an email has been also sent to {retirement.createdby} alerting the same\n\n'
                        f'VOUCHER FORM NUMBER : CR-00{retirement.ID} \n\n'
                        f'Thank you for your authorisation\n'
                        f'You can check on the dashboard if there are other forms needing your attention on the the link below: \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[self.request.user.email],
                )
                user_email.send(fail_silently=False)
            
            
                retirementowner = Staff.objects.filter(username=retirement.createdby).first()
                retirementowner_email = EmailMessage(
                    subject=f'FINALLY!!! RETIREMENT FORM NUMBER CR-00{retirement.ID} AUTHORISED',
                    body=(
                        f'Hello {retirementowner.username} ,\n\n'
                        f'Your retirement form number CR-00{retirement.ID} has been authorised at the EXECUTIVE DIRECTOR\'S OFFICE\n\n'
                        f'This means a cash tracking for this process has come to an end.\n\n'
                        f'You can be checking for the status of other forms by going on the dashboard following the link below:  \n{dashboard_url} \n\n'
                        f'Regards, \n'
                        f'CCDO Team'
                    ),
                    to=[retirementowner.email],
                )
                retirementowner_email.send(fail_silently=False)
            
                return super().form_valid(form)
        
        
class DownloadView(LoginRequiredMixin, TemplateView):
    template_name = "CashTracker/download.html"
    def get(self, request, *args, **kwargs):
       
        vouchers = Voucher.objects.filter(status__in=['Authorised', 'Done'])
        requisitions = Requisition.objects.filter(status__in=['Authorised', 'Done']) 
        retirements = Retirement.objects.filter(status__in=['Authorised', 'Done'])
        
        for requisition in requisitions:
            total_req = Item.objects.filter(requisitionid=requisition).aggregate(total=Sum('totalprice'))['total'] or 0
            requisition.total = total_req
        
        for voucher in vouchers:
            total_voucher = Item.objects.filter(requisitionid=voucher.requisitionid).aggregate(total=Sum('totalprice'))['total'] or 0
            voucher.total = total_voucher
            voucher.dept = Requisition.objects.filter(ID=voucher.requisitionid_id).first().requestingdept
            
        for retirement in retirements:
            total_retirement = Item.objects.filter(requisitionid=retirement.requisitionid_id).aggregate(total=Sum('totalprice'))['total'] or 0
            retirement.total = total_retirement
            retirement.dept = Requisition.objects.filter(ID=retirement.requisitionid_id).first().requestingdept
 
            
        

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
        finance = Staff.objects.filter(role='Finance Officer').first()
        programs = Staff.objects.filter(role='Programs Manager').first()
        ed = Staff.objects.filter(role='ED').first()
        html_string = render_to_string('CashTracker/pdf/requisition_pdf.html', {
            'requisition' : requisition,
            'items' : items,
            'total_amount' : total_amount,
            'finance' : finance,
            'programs' : programs,
            'ed' : ed,
        })
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="requisition_{requisition.ID}.pdf"'
        return response
    
class VoucherDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        voucher = Voucher.objects.get(pk=pk)
        requisition = Requisition.objects.get(pk=voucher.requisitionid_id)
        items = Item.objects.filter(requisitionid=voucher.requisitionid_id)
        total_amount = items.filter(requisitionid=voucher.requisitionid_id).aggregate(total=Sum('totalprice'))['total'] or 0
        finance = Staff.objects.filter(role='Finance Officer').first()
        programs = Staff.objects.filter(role='Programs Manager').first()
        ed = Staff.objects.filter(role='ED').first()
        html_string = render_to_string('CashTracker/pdf/voucher_pdf.html', {
            'voucher' : voucher,
            'items' : items,
            'total_amount' : total_amount,
            'finance' : finance,
            'programs' : programs,
            'ed' : ed,
            'requisition' : requisition,
        })
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="voucher_{voucher.ID}.pdf"'
        return response
    
    
class RetirementDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        retirement = Retirement.objects.get(pk=pk)
        items = Item.objects.filter(requisitionid=retirement.requisitionid_id)
        total_amount = items.filter(requisitionid=retirement.requisitionid_id).aggregate(total=Sum('totalprice'))['total'] or 0
        finance = Staff.objects.filter(role='Finance Officer').first()
        programs = Staff.objects.filter(role='Programs Manager').first()
        ed = Staff.objects.filter(role='ED').first()
        html_string = render_to_string('CashTracker/pdf/retirement_pdf.html', {
            'retirement' : retirement,
            'items' : items,
            'total_amount' : total_amount,
            'finance' : finance,
            'programs' : programs,
            'ed' : ed,
        })
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="retirement_{retirement.ID}.pdf"'
        return response