from django.urls import path
from ElBuenSaborApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Inicio, name='inicio'),
    path('check-service-status/', views.check_service_status, name='check_service_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
