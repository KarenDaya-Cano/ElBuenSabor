from pyexpat.errors import messages
from django.shortcuts import render, redirect
from CarritoApp.models import LineaPedido, Pedido
from .carrito import Carrito
from ElBuenSaborApp.models import Producto,Adicion
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .forms import AdicionForm

def Menu(request):
    lista = Producto.objects.all()
    return render(request, 'menu.html', {'productos': lista})

def pedido(request):
    productos = Producto.objects.all()
    adicion=Adicion.objects.all()
    return render(request, 'carrito.html', {'productos': productos,'adiciones':adicion})



def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('menu')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('pedido')

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('pedido')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('menu')


def procesar_pedido(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create(user=request.user)
        carrito = Carrito(request)
        lineas_pedidos = []

        for key, value in carrito.carrito.items():
            producto_id = key
            cantidad = value["cantidad"]
            producto = Producto.objects.get(id=producto_id)
            
            linea_pedido = LineaPedido(
                producto=producto,
                cantidad=cantidad,
                user=request.user,
                pedido=pedido,
            )
            linea_pedido.save()

            adicion_ids = request.POST.getlist(f'adiciones_{key}')
            for adicion_id in adicion_ids:
                adicion = Adicion.objects.get(id=adicion_id)
                linea_pedido.adiciones.add(adicion)
            
            lineas_pedidos.append(linea_pedido)

        total_pedido = pedido.total

        # Obtener datos del formulario de contacto
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        # Enviar correo electrónico con los detalles del pedido y del usuario
    def enviar_email(pedido, lineas_pedidos, nombre_usuario, email_usuario, total, nombre, direccion, telefono):
        # Construir el mensaje en formato HTML
        mensaje_html = f"""
        <p>Hola {nombre_usuario},</p>
        <p>Gracias por tu pedido. Aquí está el resumen:</p>
        <p>Nombre: {nombre}</p>
        <p>Dirección: {direccion}</p>
        <p>Teléfono: {telefono}</p>
        <p>Productos:</p>
        <ul>
        """
        for linea_pedido in lineas_pedidos:
            mensaje_html += f"<li>{linea_pedido.producto.nombre} - Cantidad: {linea_pedido.cantidad}</li>"

        mensaje_html += f"""
        </ul>
        <p>Total del pedido: {total}</p>
        """

        # Convertir el mensaje HTML a texto plano
        mensaje_texto = strip_tags(mensaje_html)

        # Configurar el correo electrónico
        asunto = "Confirmación de pedido"
        from_email = "web.kmx3@gmail.com"
        to = email_usuario

        # Enviar el correo electrónico
        send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje_html)