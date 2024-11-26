from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import AssignLeaveForm
from .models import LateNotification, LeaveWarningNotification, LeaveRequest
from personalSystem.models import LeaveUsage
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from personalSystem.models import Personal, WorkingHours
from .forms import PersonalForm

#Yetkili kişi giriş bilgilerini django superuser olanlara göre kontrol eder.
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('dashboard')  # Giriş sonrası yönlendirilecek sayfa
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
            
    return render(request, "admin_login.html")

def admin_logout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('admin_login')

def dashboard(request):
    late_notifications = LateNotification.objects.filter(is_read=False)
    leave_warnings = LeaveWarningNotification.objects.filter(is_read=False)
    pending_leave_requests = LeaveRequest.objects.filter(status='PENDING')
    
    context = {
        'late_notifications': late_notifications,
        'leave_warnings': leave_warnings,
        'pending_leave_requests': pending_leave_requests
    }
    return render(request, "dashboard.html", context)

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import LateNotification

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def notification_list(request):
    notifications = LateNotification.objects.filter(is_read=False)
    print(notifications)
    context = {
        'notifications': notifications
    }
    return render(request, 'adminSytem/notifications.html', context)

@user_passes_test(lambda u: u.is_superuser)
def assign_leave(request):
    if request.method == 'POST':
        form = AssignLeaveForm(request.POST)
        if form.is_valid():
            personal = form.cleaned_data['personal']
            days = form.cleaned_data['days']
            hours = days * 10  # 1 gün = 10 saat

            # İzin kaydını oluştur
            leave = form.save(commit=False)
            leave.hours_used = hours
            leave.save()

            # Personelin izin günlerini güncelle
            total_hours = (personal.annual_leave_days * 10) + personal.annual_leave_hours
            remaining_hours = total_hours - hours
            
            personal.annual_leave_days = remaining_hours // 10
            personal.annual_leave_hours = remaining_hours % 10
            personal.save()

            messages.success(request, f'{personal.name} {personal.surname} için {days} günlük izin tanımlandı.')
            return redirect('dashboard')
    else:
        form = AssignLeaveForm()

    return render(request, 'adminSystem/assign_leave.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def process_leave_request(request, request_id):
    print(request_id)
    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            leave_request.status = 'APPROVED'
            leave_request.processed_by = request.user
            leave_request.processed_at = timezone.now()
            
            # İzin kaydı oluştur ve izin günlerini düş
            LeaveUsage.objects.create(
                personal=leave_request.personal,
                hours_used=leave_request.requested_days * 10,
                leave_type='REQUEST',
                description=leave_request.reason
            )
            
            # Personelin izin günlerini güncelle
            personal = leave_request.personal
            total_hours = (personal.annual_leave_days * 10) + personal.annual_leave_hours
            remaining_hours = total_hours - (leave_request.requested_days * 10)
            
            personal.annual_leave_days = remaining_hours // 10
            personal.annual_leave_hours = remaining_hours % 10
            personal.save()
            
            messages.success(request, 'İzin talebi onaylandı.')
        elif action == 'reject':
            leave_request.status = 'REJECTED'
            leave_request.processed_by = request.user
            leave_request.processed_at = timezone.now()
            messages.warning(request, 'İzin talebi reddedildi.')
        
        leave_request.save()
        return redirect('dashboard')

    return render(request, 'adminSystem/process_leave_request.html', {
        'leave_request': leave_request
    })

@user_passes_test(lambda u: u.is_superuser)
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(LateNotification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')

@user_passes_test(lambda u: u.is_superuser)
def staff_reports(request):
    personals = Personal.objects.all()
    selected_personal = None
    working_hours = None
    context = {'personals': personals}
    
    if 'personal_id' in request.GET:
        selected_personal = get_object_or_404(Personal, id=request.GET['personal_id'])
        today = timezone.now().date()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        working_hours = WorkingHours.objects.filter(
            personal=selected_personal,
            date__range=[first_day, last_day]
        ).order_by('date')
        
        total_working_days = working_hours.exclude(is_weekend=True).count()
        total_hours = working_hours.aggregate(Sum('total_hours'))['total_hours__sum'] or 0
        expected_hours = total_working_days * 10
        
        context.update({
            'selected_personal': selected_personal,
            'working_hours': working_hours,
            'total_hours': total_hours,
            'expected_hours': expected_hours,
            'month': today.strftime('%B %Y')
        })
    
    return render(request, 'adminSystem/staff_reports.html', context) 


def add_personel(request):
    if request.method == 'POST':
        form =PersonalForm(request.POST)
        if form.is_valid():
            form.save()  # Personeli veritabanına kaydediyoruz
            return redirect('dashboard')  # Başarı durumunda yönlendirme
    else:
        form =PersonalForm()

    return render(request, 'adminSystem/personal_add.html', {'form': form})