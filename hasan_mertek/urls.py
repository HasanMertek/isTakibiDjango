from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('personal/', include('personalSystem.urls')),
    path('admin-system/', include('adminSytem.urls')),  # AdminSystem URL'lerini ekle
] 