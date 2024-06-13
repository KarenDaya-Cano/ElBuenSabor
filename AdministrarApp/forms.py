from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Correo o Teléfono', max_length=100, required=True)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)
    
from ElBuenSaborApp.models import Producto, Adicion

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class AdicionForm(forms.ModelForm):
    class Meta:
        model = Adicion
        fields = '__all__'

