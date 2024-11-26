from django.urls import path
from . import views

app_name = 'personalSystem'

urlpatterns = [
    path('login/', views.personal_login, name='login'),
    path('logout/', views.personal_logout, name='logout'),
    path('notifications/', views.notification_list, name='notifications'),
    path('leave-history/', views.leave_history, name='leave_history'),
    path('request-leave/', views.request_leave, name='request_leave'),
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    
] 