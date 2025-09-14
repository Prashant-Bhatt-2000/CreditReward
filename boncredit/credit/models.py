from django.db import models
from uuid import uuid4
from accounts.models import User
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal



def default_repayment_date():
    return timezone.now() + timedelta(days=30)


class CreditModel(models.Model):
    # Types of credit
    CREDIT_CHOICES = [
        ("personal_loan", "Personal Loan"),
        ("credit", "Credit"),
        ("emi", "EMI"),
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),
    ]
    
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credits")
    credit_type = models.CharField(max_length=50, choices=CREDIT_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    credit_repayment_date = models.DateTimeField(default=default_repayment_date)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    repayment_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate repayment with 10% interest
        if not self.repayment_amount:
            self.repayment_amount = self.amount * Decimal('1.10')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} - {self.credit_type} - {self.amount}"
