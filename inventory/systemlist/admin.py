from django.contrib import admin

from .models import AssetEntry

# Make Class available in admin portal (see models.py)
admin.site.register(AssetEntry)
