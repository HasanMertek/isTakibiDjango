from django.contrib import admin
from .models import Personal, PersonelLoginLog, LateNotification, LeaveUsage, WorkingHours

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'position', 'get_remaining_leave', 
                   'total_late_hours', 'created_at', 'user')
    readonly_fields = ('user', 'total_late_hours', 'annual_leave_hours')
    search_fields = ('name', 'surname', 'email')
    list_filter = ('position', 'created_at')

    def get_remaining_leave(self, obj):
        return obj.get_annual_leave_display()
    get_remaining_leave.short_description = 'Kalan İzin'

@admin.register(PersonelLoginLog)
class PersonelLoginLogAdmin(admin.ModelAdmin):
    list_display = ('get_personal_full_name', 'login_time', 'logout_time', 'late_status', 'late_duration')
    search_fields = ('personal__name', 'personal__surname')
    list_filter = ('login_time', 'is_late')

    def get_personal_full_name(self, obj):
        return f"{obj.personal.name} {obj.personal.surname}"
    get_personal_full_name.short_description = 'Personel'

    def late_status(self, obj):
        if obj.login_time.weekday() >= 5:
            return "Hafta sonu"
        return "Geç kaldı" if obj.is_late else "Zamanında"
    late_status.short_description = 'Durum'

@admin.register(LateNotification)
class LateNotificationAdmin(admin.ModelAdmin):
    list_display = ('personal', 'login_time', 'late_duration', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('personal__name', 'personal__surname')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Seçili bildirimleri okundu olarak işaretle"

@admin.register(LeaveUsage)
class LeaveUsageAdmin(admin.ModelAdmin):
    list_display = ('personal', 'date', 'hours_used', 'leave_type')
    list_filter = ('leave_type', 'date')
    search_fields = ('personal__name', 'personal__surname')


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('personal', 'date', 'total_hours', 'is_weekend')
    list_filter = ('is_weekend', 'date')
    search_fields = ('personal__name', 'personal__surname')