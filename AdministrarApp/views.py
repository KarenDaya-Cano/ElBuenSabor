from pyexpat.errors import messages
from django.shortcuts import redirect, render
from ElBuenSaborApp.models import Producto, Adicion
from .forms import ProductoForm
from django.contrib.auth.forms import AuthenticationForm # creacion del usuario y ya creado el usuario  hacer la autenticacion 
from django.contrib.auth import login, authenticate # hacer el logeo de la 

def Login(request):
    if request.method=="POST":
        form = AuthenticationForm(request,data = request.POST)#permite capturar los datos en el formulario de logeo
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')
            usuario = authenticate(username = nombre_usuario, password = contrasena)
            if usuario is not None:
                login(request,usuario)
                return redirect('admin')
            else:
                messages.error(request, 'Usuario no logeado')
        else:
            messages.error(request,'Informacion Incorrecta')
    form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

def Administrar(request):
    productos = Producto.objects.all()
    return render(request, 'administrar.html', {'productos': productos})

def administrar_adiciones(request):
    adiciones = Adicion.objects.all()
    return render(request, 'administrar_adiciones.html', {'adiciones': adiciones})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})

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

def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('admin')
    return render(request, 'eliminar_producto.html', {'producto': producto})