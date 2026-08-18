from django.db import models
from master_data.models import Jail, SHG, VegetableMaster
from django.conf import settings

from django.conf import settings
from django.db import models

from master_data.models import Jail, SHG


class Demand(models.Model):

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("ACCEPTED", "Accepted"),
        ("VERIFIED", "Verified"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("RETURNED", "Returned"),
        ("TREASURY_SUBMITTED", "Submitted to Treasury"),
    ]

    jail = models.ForeignKey(Jail,on_delete=models.PROTECT,related_name="demands")

    shg = models.ForeignKey(SHG,on_delete=models.PROTECT,related_name="demands")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="created_demands")

    target_date = models.DateField()

    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default="DRAFT")

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

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

