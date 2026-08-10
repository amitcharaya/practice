from django.db import models

class Jail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SHG(models.Model):
    name = models.CharField(max_length=255)
    jail = models.ForeignKey(Jail, on_delete=models.CASCADE, related_name='shgs')
    contact_person = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.jail.name})"

class VegetableMaster(models.Model):
    item_name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=50) # e.g., Kg, Grams, Dozen
    punjabi_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name} ({self.unit})"