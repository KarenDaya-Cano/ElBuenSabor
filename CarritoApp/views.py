from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from CarritoApp.models import LineaPedido, Pedido
from ElBuenSaborApp.models import Producto, Adicion
from .carrito import Carrito

def qr_view(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')

        # Aquí debes obtener los datos necesarios para la factura
         # Debes obtener el pedido asociado al comprobante de pago
          # Debes obtener las líneas de pedido asociadas al pedido
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        texto = request.POST.get('texto')

        pedido = None
        lineas_pedidos = []

        enviar_correo_con_comprobante(imagen, pedido, lineas_pedidos, nombre, direccion, telefono, texto)

        return redirect('pedido')  # Redirige a donde sea necesario después de enviar el correo

    return render(request, 'qr.html')


def enviar_correo_con_comprobante(imagen, pedido, lineas_pedidos, nombre, direccion, telefono, texto):
    # Preparar el correo electrónico
    subject = 'Comprobante de pago adjunto y factura del pedido'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['web.kmx3@gmail.com']  # Dirección de correo a donde enviar

    # Renderizar el contenido HTML de la factura
    html_content = render_to_string('pedido.html', {
        'pedido': pedido,
        'lineas_pedidos': lineas_pedidos,
        'nombre': nombre,
        'direccion': direccion,
        'telefono': telefono,
        'texto': texto,
    })

    # Extraer el texto sin formato del contenido HTML
    text_content = strip_tags(html_content)

    # Crear el objeto de mensaje de correo electrónico
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    # Adjuntar el comprobante de pago al correo
    msg.attach(imagen.name, imagen.read(), imagen.content_type)

    # Enviar el correo electrónico
    try:
        msg.send()
    except Exception as e:
        # Manejar errores si ocurre algún problema en el envío del correo
        print(f'Error al enviar correo electrónico: {e}')
        raise  # O maneja el error según tus requerimientos


def procesar_pedido(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create(user=request.user)
        carrito = Carrito(request)
        lineas_pedidos = []

        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        texto = request.POST.get('texto')

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
        
        enviar_email(
            pedido=pedido,
            lineas_pedidos=lineas_pedidos,
            nombre_usuario=request.user.username,
            email_usuario=request.user.email,
            total=total_pedido,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            texto=texto,
        )
        messages.success(request, "Tu pedido ha sido enviado exitosamente.")
        
        return redirect("menu")

    return redirect("pedido")




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


def enviar_email(**kwargs):
    pedido = kwargs.get("pedido")
    lineas_pedidos = kwargs.get("lineas_pedidos")
    nombre_usuario = kwargs.get("nombre_usuario")
    total = kwargs.get("total")
    
    nombre = kwargs.get("nombre")
    direccion = kwargs.get("direccion")
    telefono = kwargs.get("telefono")
    texto = kwargs.get("texto")

    mensaje = render_to_string("pedido.html", {
        "pedido": pedido,
        "lineas_pedidos": lineas_pedidos,
        "nombre_usuario": nombre_usuario,
        "total": total,
        "nombre": nombre,  
        "direccion": direccion,  
        "telefono": telefono,
        "texto": texto,
    })

    mensaje_texto = strip_tags(mensaje)

    asunto = "Muchas gracias por el pedido"
    from_email = "web.kmx3@gmail.com"   
    to = kwargs.get("email_usuario")

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)

