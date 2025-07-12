from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Staff(AbstractUser):
    position = (
        ("ED", "ED"),
        ("Programs Manager", "Programs Manager"),
        ("Programs Coordinator", "Programs Coordinator"),
        ("Project Officer", "Project Officer"),
        ("Finance Officer", "Finance Officer"),
       ( "M & E Officer", "M & E Officer"),
        ("Field Officer", "Field Officer"),
        
    )
    role = models.CharField(max_length=25, choices=position)
    
    def __str__(self):
        return self.username
    
class Requisition(models.Model):
    ID = models.CharField(primary_key=True, max_length=10)
    date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(null=False, max_length=10, default="SUBMITTED")
    staffid = models.CharField(models.ForeignKey(Staff, on_delete=models.DO_NOTHING), null=True, default="frezer")
    activityname = models.CharField(max_length=50, null=False)
    projectname = models.CharField(max_length=50, null=False)
    projectcode = models.CharField(max_length=10)
    requestingdept = models.CharField(max_length=40)
    accountnumber = models.CharField(max_length=20, null=True, default="6565")
    
    def __str__(self):
        return self.ID
    
class Item(models.Model):
    ID = models.AutoField(primary_key=True)
    requisitionid = models.ForeignKey(Requisition, on_delete=models.CASCADE, null=False, blank=False)
    itemname = models.CharField(max_length=50, null=False, blank=False)
    reason = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    unitprice = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    
    def save(self, *args, **kwargs):
        self.totalprice = self.unitprice * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.itemname} for requisition number {self.requisitionid}'
    
class Voucher(models.Model):
    ID = models.AutoField(primary_key=True)
    requisitionid = models.ForeignKey(Requisition, on_delete=models.CASCADE, max_length=20)
    # staffid = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    status = models.CharField(null=False, max_length=10, default="SUBMITTED")
    purpose = models.CharField(max_length=200, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    
    def __str__(self):
        return f'Voucher ID {self.ID}'
    
class Retirement(models.Model):
    ID = models.AutoField(primary_key=True)
    requisitionid = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    voucherid = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    status = models.CharField(null=False, max_length=10, default="SUBMITTED")
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return f'Retirement ID {self.ID} for {self.voucherid}'