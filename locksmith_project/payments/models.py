from django.db import models
from users.models import User
from services.models import ServiceRequest

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_to_locksmith = models.BooleanField(default=False)
    razorpay_payout_id = models.CharField(max_length=100, null=True, blank=True)  # Track Razorpay payout

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.service_request.description}"

