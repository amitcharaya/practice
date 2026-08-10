from django.db import models
from master_data.models import Jail, SHG, VegetableMaster
from django.conf import settings

class Demand(models.Model):
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted'), ('ACCEPTED', 'Accepted')]
    jail = models.ForeignKey(Jail, on_delete=models.CASCADE)
    shg = models.ForeignKey(SHG, on_delete=models.CASCADE)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demand {self.id} from {self.jail.name} to {self.shg.name}"

class DemandItem(models.Model):
    demand = models.ForeignKey(Demand, related_name='items', on_delete=models.CASCADE)
    vegetable = models.ForeignKey(VegetableMaster, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Requested quantity by Jail")
    confirmed_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Confirmed quantity supplied by SHG")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price per Kg set by SHG")

    def __str__(self):
        return f"{self.demand} - {self.vegetable.item_name} - {self.quantity} Kg"

class Order(models.Model):
    demand = models.OneToOneField(Demand, on_delete=models.CASCADE)
    shg = models.ForeignKey(SHG, on_delete=models.PROTECT)
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for Demand {self.demand.id} to SHG {self.shg.name}"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('VERIFIED_JU', 'Verified by Jail User'),
        ('APPROVED_JA', 'Approved by Jail Admin'),
        ('SUBMITTED_TREASURY', 'Submitted to Treasury'),
        ('REJECTED', 'Rejected'),
        ('PAID', 'Paid'),
    ]
    order = models.ForeignKey(Order, related_name='invoices', on_delete=models.CASCADE)
    shg_invoice_file = models.FileField(upload_to='invoices/shg/', null=True, blank=True)
    shg_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    remarks = models.TextField(blank=True, null=True)
    approval_file = models.FileField(upload_to='approvals/', null=True, blank=True)
    
    # Payment fields
    payment_ref = models.CharField(max_length=100, blank=True, null=True)
    payment_mode = models.CharField(max_length=50, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    treasury_bill_no = models.CharField(max_length=100, blank=True, null=True)
    treasury_submission_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for Order {self.order.id} - Status: {self.status}"

class OrderHistory(models.Model):
    order = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=100)  # e.g., "ORDER_CREATED", "INVOICE_UPLOADED"
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} by {self.performed_by} on {self.timestamp}"