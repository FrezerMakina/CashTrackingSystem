from django.urls import path, include
from .views import *
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard' ),
    path('requisition/', RequisitionView.as_view(), name='requisition' ),
    path('voucher/', VoucherView.as_view(), name='voucher' ),
    path('retirement/', RetirementView.as_view(), name='retirement' ),
    path('download/', DownloadView.as_view(), name='download' ),
]