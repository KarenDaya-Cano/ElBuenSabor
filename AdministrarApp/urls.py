from django.urls import path
from AdministrarApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login',views.Login, name='login'),
    path('administrar',views.Administrar, name='admin'),
    path('administrar/adiciones/', views.administrar_adiciones, name='administrar_adiciones'),
    path('administrar/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('administrar/productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('administrar/productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
