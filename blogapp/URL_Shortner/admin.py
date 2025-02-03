from django.contrib import admin

# Register your models here.

from .models import LongToShort,  ClickAnalytics


admin.site.register(LongToShort)

admin.site.register(ClickAnalytics)
