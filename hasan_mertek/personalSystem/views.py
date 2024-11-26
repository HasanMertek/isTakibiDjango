from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import PersonelLoginLog, LateNotification, LeaveUsage, WorkingHours
from django.utils import timezone
from datetime import time, timedelta
from .signals import calculate_late_duration
from .forms import LeaveRequestForm
from adminSytem.models import LeaveRequest
from django.db.models import Sum

def can_login(user):
    current_time = timezone.localtime().time()
    end_time = time(18, 00)  # 18:00
    
    # Eğer kullanıcı superuser ise her zaman giriş yapabilir
    if user.is_superuser:
        return True
    
    # 18:00'dan sonra ise ve superuser değilse giriş yapamaz
    if current_time >= end_time:
        return False
    
    return True

@user_passes_test(lambda u: not u.is_superuser, login_url='/')
def personal_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username = email.split('@')[0]
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Mesai saati kontrolü
            current_time = timezone.localtime().time()
            end_time = time(18, 00)  # 18:00
            
            if current_time >= end_time and not user.is_superuser:
                messages.error(request, 'Mesai saati (18:00) sonrası sadece yöneticiler giriş yapabilir!')
                return redirect('personalSystem:login')
            
            login(request, user)
            
            # Login log işlemleri
            existing_log = PersonelLoginLog.objects.filter(
                personal=user.personal,
                logout_time__isnull=True
            ).first()
            
            if not existing_log:
                current_time = timezone.now()
                late_duration, is_late, late_hours = calculate_late_duration(current_time)
                
                PersonelLoginLog.objects.create(
                    personal=user.personal,
                    login_time=current_time,
                    late_duration=late_duration if late_duration else None,
                    is_late=is_late
                )
            
            return redirect('dashboard')
        else:
            messages.error(request, 'Geçersiz email veya parola!')
            
    return render(request, 'personalSystem/login.html')

def personal_logout(request):
    if request.user.is_authenticated:
        # En son açık olan login kaydını bul
        last_login = PersonelLoginLog.objects.filter(
            personal=request.user.personal,
            logout_time__isnull=True
        ).first()
        
        if last_login:
            last_login.logout_time = timezone.now()
            last_login.save()
    
    logout(request)
    return redirect('personalSystem:login')

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def notification_list(request):
    notifications = LateNotification.objects.filter(is_read=False)
    return render(request, 'personalSystem/notifications.html', {
        'notifications': notifications
    })

@login_required
def leave_history(request):
    personal = request.user.personal
    leave_usages = LeaveUsage.objects.filter(personal=personal)
    context = {
        'personal': personal,
        'leave_usages': leave_usages,
        'remaining_leave': personal.get_annual_leave_display(),
        'total_late_hours': personal.total_late_hours
    }
    return render(request, 'personalSystem/leave_history.html', context)

@login_required
def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.user.personal, request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.personal = request.user.personal
            leave_request.save()
            messages.success(request, 'İzin talebiniz başarıyla oluşturuldu.')
            
            return redirect('dashboard')
    else:
        form = LeaveRequestForm(request.user.personal)
    
    return render(request, 'personalSystem/request_leave.html', {'form': form})

@login_required
def monthly_report(request):
    today = timezone.now().date()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    working_hours = WorkingHours.objects.filter(
        personal=request.user.personal,
        date__range=[first_day, last_day]
    ).order_by('date')
    
    # Aylık özet istatistikler
    total_working_days = working_hours.exclude(is_weekend=True).count()
    total_hours = working_hours.aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    expected_hours = total_working_days * 10  # 10 saat/gün
    
    context = {
        'working_hours': working_hours,
        'total_hours': total_hours,
        'expected_hours': expected_hours,
        'month': today.strftime('%B %Y')
    }
    return render(request, 'personalSystem/monthly_report.html', context)
