from django.urls import path
from . import views

App_name='CarritoApp'
urlpatterns = [
    path('pedido/', views.pedido, name='pedido'),
    path('menu/', views.Menu, name='menu'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='add'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='del'),
    path('restar/<int:producto_id>/', views.restar_producto, name='sub'),
    path('limpiar/', views.limpiar_carrito, name='cls'),
    path('procesar_pedido/', views.procesar_pedido, name = 'procesar_pedidos'),
    path('qr/', views.qr_view, name='qr'),
]
