from django.urls import path
from . import views

app_name = 'adminSytem'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assign-leave/', views.assign_leave, name='assign_leave'),
    path('process-leave-request/<int:request_id>/', views.process_leave_request, name='process_leave_request'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('staff-reports/', views.staff_reports, name='staff_reports'),
    path('personel-ekle/', views.add_personel, name='personel_add'),  # Personel ekleme URL'si


] 