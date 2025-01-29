from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='service_requests')
    locksmith = models.ForeignKey('locksmiths.LocksmithProfile', on_delete=models.SET_NULL, null=True, blank=True)
    service_category = models.ForeignKey('services.ServiceCategory', on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service_category.name}"
