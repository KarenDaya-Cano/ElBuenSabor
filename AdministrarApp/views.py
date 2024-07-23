from django.shortcuts import redirect, render
from ElBuenSaborApp.models import Producto, Adicion
from .forms import ProductoForm, AdicionForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate, logout 
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from CarritoApp.models import Producto, LineaPedido
from django.db.models import Sum, F
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
import csv

def start_service(request):
    cache.set('service_status', 'active')
    return JsonResponse({'success': True})

def stop_service(request):
    cache.set('service_status', 'inactive')
    return JsonResponse({'success': True})

def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')
            usuario = authenticate(username=nombre_usuario, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect('botones')
            else:
                messages.error(request, 'Usuario no logeado')
        else:
            messages.error(request, 'Información incorrecta')
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

def custom_error_view(request, exception):
    return render(request, 'custom_error_view.html', {"message": 'Página no válida para usuarios'})

@login_required
def Botones(request):
    return render(request, "botones.html", {})

@login_required
def dashboard(request):
    product_count = Producto.objects.count()
    addition_count = Adicion.objects.count()
    return render(request, 'dashboard.html', {
        'product_count': product_count,
        'addition_count': addition_count
    })

@login_required
def Administrar(request):
    productos = Producto.objects.all()
    return render(request, 'administrar.html', {'productos': productos})

@login_required
def administrar_adiciones(request):
    adiciones = Adicion.objects.all()
    return render(request, 'administrar_adiciones.html', {'adiciones': adiciones})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('admin')
    return render(request, 'eliminar_producto.html', {'producto': producto})

@login_required
def agregar_adicion(request):
    if request.method == 'POST':
        form = AdicionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('administrar_adiciones') 
    else:
        form = AdicionForm()
    return render(request, 'agregar_adicion.html', {'form': form})

@login_required
def editar_adicion(request, pk):
    adicion = Adicion.objects.get(pk=pk)
    if request.method == 'POST':
        form = AdicionForm(request.POST, request.FILES, instance=adicion)
        if form.is_valid():
            form.save()
            return redirect('administrar_adiciones')  
    else:
        form = AdicionForm(instance=adicion)
    return render(request, 'editar_adicion.html', {'form': form})

@login_required
def eliminar_adicion(request, pk):
    adicion = Adicion.objects.get(pk=pk)
    if request.method == 'POST':
        adicion.delete()
        return redirect('administrar_adiciones')  
    return render(request, 'eliminar_adicion.html', {'adicion': adicion})

@login_required
def dashboard(request):
    product_count = Producto.objects.count()
    addition_count = Adicion.objects.count()
    return render(request, 'dashboard.html', {
        'product_count': product_count,
        'addition_count': addition_count
    })

@login_required
def reporte_ventas(request):
    fecha_actual = date.today()
    ventas_por_producto = LineaPedido.objects.filter(
        pedido__created__date=fecha_actual
    ).values('producto__producto').annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos_totales=Sum(F('cantidad') * F('producto__precio'))
    )
    return render(request, 'reporte.html', {'ventas_por_producto': ventas_por_producto})

def reporte_ventas_pdf(request):
    fecha_actual = date.today()

    ventas_por_producto = LineaPedido.objects.filter(
        pedido__created__date=fecha_actual
    ).values('producto__producto').annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos_totales=Sum(F('cantidad') * F('producto__precio'))
    )

    template_path = 'reporte_pdf.html'
    context = {'ventas_por_producto': ventas_por_producto, 'fecha_actual': fecha_actual}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    pisa_status = pisa.CreatePDF(
       html, dest=response
    )
    return response



def reporte_ventas_csv(request):
    fecha_actual = date.today()

    ventas_por_producto = LineaPedido.objects.filter(
        pedido__created__date=fecha_actual
    ).values('producto__producto').annotate(
        cantidad_vendida=Sum('cantidad'),
        ingresos_totales=Sum(F('cantidad') * F('producto__precio'))
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Producto', 'Cantidad Vendida', 'Ingresos Totales'])

    for venta in ventas_por_producto:
        writer.writerow([
            venta['producto__producto'],  
            venta['cantidad_vendida'],    
            venta['ingresos_totales'],    
        ])
    return response