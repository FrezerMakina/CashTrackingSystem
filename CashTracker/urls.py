from django.conf import settings
from django.conf.urls.static import static


from django.urls import path, include
from .views import *
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard' ),
    path('requisition/', RequisitionView.as_view(), name='requisition' ),
    path('voucher/', VoucherView.as_view(), name='voucher' ),
    path('voucher/<int:requisitionid>/', VoucherajaxView.as_view(), name='voucherajax' ),
    # path('voucher/', VoucherView.as_view(), name='voucher' ),
    path('retirement/', RetirementView.as_view(), name='retirement' ),
    path('retirement/<int:voucherid>/', RetirementajaxView.as_view(), name='retirementajax' ),
    path('download/', DownloadView.as_view(), name='download' ),
    
    path('requisition/<int:pk>/review/', RequisitionReviewView.as_view(), name='requisitionreview'),
    path('voucher/<int:pk>/review/', VoucherReviewView.as_view(), name='voucherreview'),
    path('retirement/<int:pk>/review/', RetirementReviewView.as_view(), name='retirementreview'),
    
    path('items/<int:requisitionid>/', ItemsajaxView.as_view(), name='itemsajax' ),
    
    path('download/requisition/<int:pk>/', RequisitionDownloadView.as_view(), name='requisitiondownload'),
    path('download/voucher/<int:pk>/', VoucherDownloadView.as_view(), name='voucherdownload'),
    path('download/retirement/<int:pk>/', RetirementDownloadView.as_view(), name='retirementdownload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)