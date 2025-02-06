from django.contrib import admin
from .models import LocksmithProfile

class LocksmithProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "get_location", "service_radius_km", "approved")
    list_filter = ("approved",)
    search_fields = ("user__username", "business_name")

    def get_location(self, obj):
        """Display latitude and longitude as a single string"""
        return f"Lat: {obj.location_latitude}, Lon: {obj.location_longitude}"

    get_location.short_description = "Location"

admin.site.register(LocksmithProfile, LocksmithProfileAdmin)
