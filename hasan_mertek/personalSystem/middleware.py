from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import time

class WorkingHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            current_time = timezone.localtime().time()
            end_time = time(18, 00)

            if current_time >= end_time:
                messages.warning(request, 'Mesai saati sona erdi. Sistemden çıkış yapılıyor.')
                return redirect('admin_logout')

        return self.get_response(request) 