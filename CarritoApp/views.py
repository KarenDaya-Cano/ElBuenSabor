import email
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
import requests
from CarritoApp.models import LineaPedido, Pedido
from ElBuenSaborApp.models import Producto, Adicion
from .carrito import Carrito
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def Menu(request):
    lista_productos = Producto.objects.all()
    lista_adiciones = Adicion.objects.all()
    return render(request, 'menu.html', {'productos': lista_productos, 'adiciones': lista_adiciones})

def pedido(request):
    lista_productos = Producto.objects.all()
    lista_adiciones = Adicion.objects.all()
    return render(request, 'carrito.html', {'productos': lista_productos, 'adiciones': lista_adiciones})

def comprar(request):
    lista_productos = Producto.objects.all()
    lista_adiciones = Adicion.objects.all()
    return render(request, 'info.html', {'productos': lista_productos, 'adiciones': lista_adiciones})

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    messages.success(request, f'El producto {producto} se ha agregado al carrito.')
    return redirect('menu')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    messages.warning(request, f'El producto {producto} se ha eliminado del carrito.')
    return redirect('pedido')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    messages.warning(request, f'Se ha restado 1 unidad del producto {producto}.')
    return redirect('pedido')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    messages.info(request, 'El carrito se ha vaciado.')
    return redirect('menu')
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives

def procesar_pedido(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create()
        carrito = Carrito(request)
        lineas_pedidos = []
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        texto = request.POST.get('texto')
        imagen_file = request.FILES.get('imagen')

        for key, value in carrito.carrito.items():
            producto_id = key
            cantidad = value["cantidad"]
            producto = Producto.objects.get(id=producto_id)
            linea_pedido = LineaPedido(
                producto=producto,
                cantidad=cantidad,
                pedido=pedido,
            )
            linea_pedido.save()
            adicion_ids = request.POST.getlist(f'adiciones_{key}')
            for adicion_id in adicion_ids:
                adicion = Adicion.objects.get(id=adicion_id)
                linea_pedido.adiciones.add(adicion)
            lineas_pedidos.append(linea_pedido)
        total_pedido = sum([lp.sub_total() for lp in lineas_pedidos])

        enviar_email(
            pedido=pedido,
            lineas_pedidos=lineas_pedidos,
            nombre_usuario=nombre,
            email_usuario="web.kmx3@gmail.com",
            total=total_pedido,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            texto=texto,
            imagen_file=imagen_file,  # Enviar el archivo de imagen
        )
        messages.success(request, "Tu pedido ha sido enviado exitosamente.")
        return redirect("menu")
    return redirect("pedido")

from django.core.mail import EmailMultiAlternatives

def enviar_email(**kwargs):
    pedido = kwargs.get("pedido")
    lineas_pedidos = kwargs.get("lineas_pedidos")
    nombre_usuario = kwargs.get("nombre_usuario")
    total = kwargs.get("total")
    nombre = kwargs.get("nombre")
    direccion = kwargs.get("direccion")
    telefono = kwargs.get("telefono")
    texto = kwargs.get("texto")
    imagen_file = kwargs.get("imagen_file")

    mensaje_html = render_to_string("pedido.html", {
        "pedido": pedido,
        "lineas_pedidos": lineas_pedidos,
        "nombre_usuario": nombre_usuario,
        "total": total,
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "texto": texto,
    })
    mensaje_texto = strip_tags(mensaje_html)
    asunto = "Muchas gracias por el pedido"
    from_email = "web.kmx3@gmail.com"
    to = kwargs.get("email_usuario", "web.kmx3@gmail.com")

    email = EmailMultiAlternatives(asunto, mensaje_texto, from_email, [to])
    email.attach_alternative(mensaje_html, "text/html")

    if imagen_file:
        # Adjunta el archivo de imagen al correo
        email.attach(imagen_file.name, imagen_file.read(), imagen_file.content_type)

    email.send()
