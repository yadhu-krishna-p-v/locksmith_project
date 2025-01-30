from django.contrib import admin
from .models import LocksmithProfile

class LocksmithProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'location', 'approved')
    list_filter = ('approved',)
    actions = ['approve_locksmith']

    def approve_locksmith(self, request, queryset):
        queryset.update(approved=True)
    approve_locksmith.short_description = "Approve selected locksmiths"

admin.site.register(LocksmithProfile, LocksmithProfileAdmin)
