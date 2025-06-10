from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Staff)
admin.site.register(Requisition)
admin.site.register(Voucher)
admin.site.register(Retirement)
admin.site.register(Item)