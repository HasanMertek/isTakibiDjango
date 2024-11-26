from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time

# Create your models here.
class Personal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=100)
    annual_leave_days = models.IntegerField(default=15)
    annual_leave_hours = models.IntegerField(default=0)
    total_late_hours = models.FloatField(default=0.0)

    def update_annual_leave(self, late_hours):
        # Geç kalma saatini tam sayıya yuvarla
        late_hours = round(late_hours)
        
        # Mevcut izin durumunu saate çevir
        total_hours = (self.annual_leave_days * 10) + self.annual_leave_hours
        
        # Geç kalınan saati düş
        remaining_hours = total_hours - late_hours
        
        # Günleri ve saatleri hesapla
        self.annual_leave_days = remaining_hours // 10
        self.annual_leave_hours = remaining_hours % 10
        
        self.total_late_hours += late_hours
        self.save()

    def get_annual_leave_display(self):
        if self.annual_leave_hours > 0:
            return f"{self.annual_leave_days} gün {self.annual_leave_hours} saat"
        return f"{self.annual_leave_days} gün"

    def __str__(self):
        return f"{self.name} {self.surname}"

    def check_leave_threshold(self):
        total_days = self.annual_leave_days + (self.annual_leave_hours / 10)
        if total_days <= 3:
            from adminSytem.models import LeaveWarningNotification
            LeaveWarningNotification.objects.create(
                personal=self,
                remaining_leave=self.get_annual_leave_display(),
                message=f"Dikkat! {self.name} {self.surname}'in kalan izin süresi {self.get_annual_leave_display()}"
            )

class PersonelLoginLog(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    late_duration = models.CharField(max_length=50, null=True, blank=True)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.personal} - {self.login_time.date()}"

class LateNotification(models.Model):
    personal = models.ForeignKey('Personal', on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    late_duration = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.personal} - {self.late_duration} geç kaldı"

    class Meta:
        ordering = ['-created_at']

class LeaveUsage(models.Model):
    LEAVE_TYPES = (
        ('LATE', 'Geç Kalma'),
        ('REQUEST', 'İzin Talebi'),
    )

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='leave_usages')
    date = models.DateField(auto_now_add=True)
    hours_used = models.FloatField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    description = models.TextField()

    def __str__(self):
        return f"{self.personal} - {self.get_leave_type_display()} - {self.hours_used} saat"

    class Meta:
        ordering = ['-date']

class WorkingHours(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='working_hours')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_weekend = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['personal', 'date']

    def save(self, *args, **kwargs):
        # Cumartesi veya Pazar ise is_weekend=True
        if self.date.weekday() >= 5:  # 5=Cumartesi, 6=Pazar
            self.is_weekend = True
        
        # Çalışma saatlerini hesapla
        if self.check_in and self.check_out:
            start = datetime.combine(self.date, self.check_in)
            end = datetime.combine(self.date, self.check_out)
            
            # Normal mesai saatleri
            workday_start = datetime.combine(self.date, time(8, 0))
            workday_end = datetime.combine(self.date, time(18, 0))
            
            # Geç gelme ve erken çıkmaları hesapla
            actual_start = max(start, workday_start)
            actual_end = min(end, workday_end)
            
            duration = actual_end - actual_start
            self.total_hours = duration.total_seconds() / 3600  # Saat cinsinden
        
        super().save(*args, **kwargs)

