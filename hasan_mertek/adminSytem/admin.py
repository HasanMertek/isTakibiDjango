from django.contrib import admin
from .models import LateNotification, LeaveWarningNotification, LeaveRequest

@admin.register(LateNotification)
class LateNotificationAdmin(admin.ModelAdmin):
    list_display = ('personal', 'login_time', 'late_duration', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('personal__name', 'personal__surname')

@admin.register(LeaveWarningNotification)
class LeaveWarningNotificationAdmin(admin.ModelAdmin):
    list_display = ('personal', 'remaining_leave', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('personal__name', 'personal__surname')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('personal', 'requested_days', 'status', 'created_at')
    
    