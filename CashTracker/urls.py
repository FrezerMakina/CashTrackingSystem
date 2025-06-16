from django.urls import path, include
from .views import *
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard' ),
]