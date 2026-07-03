from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WeightHistory

admin.site.register(CustomUser, UserAdmin)
# Register your models here.

@admin.register(WeightHistory)
class WeightHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'recorded_at')
    list_filter = ('user', 'recorded_at')
