from django.db import models


class LocksmithProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='locksmith_profile')
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    location_latitude = models.FloatField()  # Locksmith's latitude
    location_longitude = models.FloatField()  # Locksmith's longitude
    service_radius_km = models.IntegerField(default=10)
    approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return self.business_name
    

class LocksmithService(models.Model):
    """Services offered by a locksmith with pricing"""
    locksmith = models.ForeignKey("locksmiths.LocksmithProfile", on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey("services.ServiceCategory", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    car_manufacturer = models.CharField(max_length=255, null=True, blank=True)  # For car key services
    car_model = models.CharField(max_length=255, null=True, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    key_features = models.TextField(null=True, blank=True)  # Smart keys, transponder, etc.

    def __str__(self):
        return f"{self.locksmith.user.username} - {self.category.name}"

