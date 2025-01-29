from django.db import models

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    service_request = models.ForeignKey('services.ServiceRequest', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_to_locksmith = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount}"

