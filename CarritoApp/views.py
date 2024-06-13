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
        lineas_pedidos = list()
        
        for key, value in carrito.carrito.items():
            producto_id = key
            cantidad = value["cantidad"]
            producto = Producto.objects.get(id=producto_id)
            
            # Crear y guardar LineaPedido antes de agregar adiciones
            linea_pedido = LineaPedido(
                producto=producto,
                cantidad=cantidad,
                user=request.user,
                pedido=pedido,
            )
            linea_pedido.save()  # Guardar para que obtenga un ID

            # Agregar adiciones seleccionadas para este producto
            adicion_ids = request.POST.getlist(f'adiciones_{key}')
            for adicion_id in adicion_ids:
                adicion = Adicion.objects.get(id=adicion_id)
                linea_pedido.adiciones.add(adicion)
            
            lineas_pedidos.append(linea_pedido)

        # No usar bulk_create porque ya guardamos individualmente
        total_pedido = pedido.total  # Aquí se agrega el total al contexto
        
        enviar_email(
            pedido=pedido,
            lineas_pedidos=lineas_pedidos,
            nombre_usuario=request.user.username,
            email_usuario=request.user.email,
            total=total_pedido  # se agrega el total al enviar
        )

        return redirect("menu")

    return redirect("pedidoo")

def enviar_email(**kwargs):
    asunto = "Muchas gracias por el pedido"
    mensaje = render_to_string("pedido.html", {
        "pedido":kwargs.get("pedido"),
        "lineas_pedidos": kwargs.get("lineas_pedidos"),
        "nombre_usuario":kwargs.get("nombre_usuario"),
        "total":kwargs.get("total") # Se obtiene el total
    })

    mensaje_texto = strip_tags (mensaje)
    from_email = "web.kmx3@gmail.com"   
    to = kwargs.get("email_usuario")
    #to = "karencano1123@gmail.com"

    send_mail(asunto, mensaje_texto, from_email, [to], html_message = mensaje)