from django.urls import path
from AdministrarApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login',views.Login, name='login'),
    path('botones/',views.Botones, name='botones'),
    path('administrar/',views.Administrar, name='admin'),
    path('administrar/adiciones/', views.administrar_adiciones, name='administrar_adiciones'),
    path('administrar/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('administrar/productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('administrar/productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'), 
    path('administrar/adiciones/agregar/', views.agregar_adicion, name='agregar_adicion'),
    path('administrar/adiciones/editar/<int:pk>/', views.editar_adicion, name='editar_adicion'),
    path('administrar/adiciones/eliminar/<int:pk>/', views.eliminar_adicion, name='eliminar_adicion'),  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
