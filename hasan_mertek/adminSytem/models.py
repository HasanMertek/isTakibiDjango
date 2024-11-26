from django.db import models
from django.contrib.auth.models import User
from personalSystem.models import Personal


class LateNotification(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='admin_notifications')
    login_time = models.DateTimeField()
    late_duration = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.personal} - {self.late_duration} geç kaldı"

    class Meta:
        ordering = ['-created_at'] 

class LeaveWarningNotification(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    remaining_leave = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.personal} - Kalan İzin: {self.remaining_leave}"

    class Meta:
        ordering = ['-created_at'] 

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Beklemede'),
        ('APPROVED', 'Onaylandı'),
        ('REJECTED', 'Reddedildi'),
    )

    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='admin_leave_requests')
    requested_days = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_leave_requests')

    def __str__(self):
        return f"{self.personal} - {self.requested_days} gün - {self.get_status_display()}"

    class Meta:
        ordering = ['-created_at'] 

            