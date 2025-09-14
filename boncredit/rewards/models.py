from django.db import models
from uuid import uuid4
from accounts.models import User
from credit.models import CreditModel
from payment.models import PaymentModel

class RewardModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rewards")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # reward value
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - Reward: {self.amount}"

    def eligible_for_reward(self) -> bool:
      
        last_3_payments = (
            PaymentModel.objects
            .filter(user=self.user, status="COMPLETED")
            .select_related("credit")
            .order_by("-created_at")[:3]
        )

        # Must have at least 3 completed payments
        if last_3_payments.count() < 3:
            return False

        for payment in last_3_payments:
            credit = payment.credit
            if not credit or payment.created_at > credit.credit_repayment_date:
                return False

        return True
