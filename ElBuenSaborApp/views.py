from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

def check_service_status(request):
    status = cache.get('service_status', 'active')
    return JsonResponse({'status': status})

def Inicio(request):
    return render(request, 'inicio.html', {})