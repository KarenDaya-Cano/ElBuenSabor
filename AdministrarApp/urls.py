from django.urls import path
from AdministrarApp import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler403 #modifique para mensaje de error
handler403 = views.custom_error_view

urlpatterns = [
    path('login',views.Login, name='login'),
    path('cerrar_sesion',views.cerrar_sesion, name="cerrar_sesion"),
    path('botones/',views.Botones, name='botones'),
    path('administrar/',views.Administrar, name='administrar_producto'),
    path('administrar/adiciones/', views.administrar_adiciones, name='administrar_adiciones'),
    path('administrar/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('administrar/productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'), 
    path('administrar/adiciones/agregar/', views.agregar_adicion, name='agregar_adicion'),
    path('administrar/adiciones/editar/<int:pk>/', views.editar_adicion, name='editar_adicion'),
    path('eliminar-adicion/<int:pk>/', views.eliminar_adicion, name='eliminar_adicion'),
    path('start-service/', views.start_service, name='start_service'),
    path('stop-service/', views.stop_service, name='stop_service'),
    path('dashboard/',views. dashboard, name='dashboard'),
    path('reporte-ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('reporte-ventas/csv/', views.reporte_ventas_csv, name='reporte_ventas_csv'),
    path('reporte-ventas/pdf/', views.reporte_ventas_pdf, name='reporte_ventas_pdf'),   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
