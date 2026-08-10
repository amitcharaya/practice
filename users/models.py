from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    SUPER_ADMIN = 'SA', 'Super Admin'
    JAIL_ADMIN = 'JA', 'Jail Admin'
    JAIL_USER = 'JU', 'Jail User'
    SHG_USER = 'SHG', 'SHG User'
    FINANCE = 'FIN', 'Finance Department'

class User(AbstractUser):
    role = models.CharField(max_length=5, choices=Role.choices)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)  # For Google Authenticator
    jail = models.ForeignKey('master_data.Jail', on_delete=models.SET_NULL, null=True, blank=True)
    shg = models.ForeignKey('master_data.SHG', on_delete=models.SET_NULL, null=True, blank=True)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"
