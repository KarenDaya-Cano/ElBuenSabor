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
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        texto = request.POST.get('texto')

        # Obtener el pedido y las líneas de pedido
        pedido = Pedido.objects.latest('id')
        lineas_pedidos = LineaPedido.objects.filter(pedido=pedido)

        if not pedido or not lineas_pedidos:
            return redirect('error_page')  # Manejo de error si no se encuentran datos

        total = sum(linea.sub_total() for linea in lineas_pedidos)

        # Enviar el correo con el comprobante y la factura
        enviar_correo_con_comprobante(imagen, pedido, lineas_pedidos, nombre, direccion, telefono, texto, total)

        return redirect('pedido')  # Redirige a la página deseada después de enviar el correo

    return render(request, 'qr.html')





def enviar_correo_con_comprobante(imagen, pedido, lineas_pedidos, nombre, direccion, telefono, texto, total):
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
        'total': total  # Asegúrate de incluir el total aquí
    })

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    # Adjuntar el comprobante de pago al correo
    if imagen:
        msg.attach(imagen.name, imagen.read(), imagen.content_type)

    try:
        msg.send()
    except Exception as e:
        print(f'Error al enviar correo electrónico: {e}')
        raise



def procesar_pedido(request):
    if request.method == 'POST':
        # Crea el pedido sin usuario asociado
        pedido = Pedido.objects.create()

        carrito = Carrito(request)
        lineas_pedidos = []

        # Obtén los datos del formulario
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        texto = request.POST.get('texto')

        for key, value in carrito.carrito.items():
            producto_id = key
            cantidad = value["cantidad"]
            producto = Producto.objects.get(id=producto_id)
            
            # Crear la línea de pedido sin usuario
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

        # Calcula el total del pedido
        total_pedido = sum([lp.sub_total() for lp in lineas_pedidos])
        
        # Llama a la función para enviar el correo electrónico, asegurando que se envíe al correo deseado
        enviar_email(
            pedido=pedido,
            lineas_pedidos=lineas_pedidos,
            nombre_usuario=nombre,  # En este caso, nombre del usuario se usa como nombre del remitente
            email_usuario="web.kmx3@gmail.com",  # Enviar siempre a esta dirección
            total=total_pedido,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            texto=texto,  # Asegúrate de incluir el texto aquí
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
    to = kwargs.get("email_usuario", "web.kmx3@gmail.com")  # Asegura que siempre tenga un valor

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)