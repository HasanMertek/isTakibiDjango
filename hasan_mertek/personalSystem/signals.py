from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Personal, PersonelLoginLog, LateNotification, LeaveUsage
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in, user_logged_out
from datetime import datetime, time
from adminSytem.models import LateNotification

def calculate_late_duration(login_time):
    work_start_time = time(8, 0)  # 08:00
    expected_time = datetime.combine(login_time.date(), work_start_time)
    expected_time = timezone.make_aware(expected_time)
    
    if login_time.weekday() >= 5:  # Hafta sonu kontrolü
        return None, False, 0
    
    if login_time > expected_time:
        late_timedelta = login_time - expected_time
        late_hours = round(late_timedelta.seconds / 3600)
        
        hours = late_hours
        minutes = round((late_timedelta.seconds % 3600) / 60)
        
        if hours > 0:
            late_str = f"{hours} saat {minutes} dakika geç"
        else:
            late_str = f"{minutes} dakika geç"
            
        return late_str, True, late_hours
    
    return None, False, 0

def create_late_notification(personal, login_time, late_duration):
    # Tüm superuser'lara bildirim gönder
    LateNotification.objects.create(
        personal=personal,
        login_time=login_time,
        late_duration=late_duration
    )

@receiver(post_save, sender=Personal)
def create_user_for_personal(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Kullanıcı adını email'den oluştur
        username = instance.email.split('@')[0]
        
        # Yeni user oluştur
        user = User.objects.create(
            username=username,
            email=instance.email,
            password=make_password(instance.password),  # Parolayı hash'le
            first_name=instance.name,
            last_name=instance.surname
        )
        
        # Personal ile User'ı ilişkilendir
        instance.user = user
        instance.save() 

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if hasattr(user, 'personal'):
        current_time = timezone.now()
        late_duration, is_late, late_hours = calculate_late_duration(current_time)
        
        if is_late and late_duration:
            # Geç kalma kaydını oluştur
            LeaveUsage.objects.create(
                personal=user.personal,
                hours_used=late_hours,
                leave_type='LATE',
                description=f'Mesaiye {late_duration} geç kalındı.'
            )
            
            # Yıllık izinden düş
            user.personal.update_annual_leave(late_hours)
            
            # Bildirim oluştur
            LateNotification.objects.create(
                personal=user.personal,
                login_time=current_time,
                late_duration=late_duration
            )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user and hasattr(user, 'personal'):
        last_login = PersonelLoginLog.objects.filter(
            personal=user.personal,
            logout_time__isnull=True
        ).first()
        
        if last_login:
            last_login.logout_time = timezone.now()
            last_login.save()

@receiver(post_save, sender=Personal)
def check_leave_days(sender, instance, **kwargs):
    total_days = instance.annual_leave_days + (instance.annual_leave_hours / 10)
    if total_days <= 3:
        instance.check_leave_threshold()