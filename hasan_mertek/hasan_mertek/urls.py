"""
URL configuration for hasan_mertek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from adminSytem.views import admin_login, admin_logout, dashboard, assign_leave,add_personel
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',admin_login, name="admin_login"),
    path("administator-login/", admin_login, name="admin_login"),
    path("administator-logout/", admin_logout, name="admin_logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path('personal/', include('personalSystem.urls')),
    path('admin-system/', include('adminSytem.urls')),
    path('assign-leave/', assign_leave, name='assign_leave'),
    path('personel-ekle/', add_personel, name='personal_add'),

]
