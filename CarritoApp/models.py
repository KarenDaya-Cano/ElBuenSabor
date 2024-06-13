from django.db import models
from django.contrib.auth import get_user_model
from ElBuenSaborApp.models import Adicion, Producto
from django.db.models import F, Sum, FloatField


User = get_user_model()
class Pedido(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

    def __str__(self):
        return self.id
    
    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            total = Sum(F("producto__precio")*F("cantidad"), output_field = FloatField())
        )["total"]
    
class LineaPedido(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    adiciones = models.ManyToManyField(Adicion, blank=True)  # Relación con las adiciones seleccionadas
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lineapedido'
        verbose_name = 'linea pedido'
        verbose_name_plural = 'linea pedidos'

    def __str__(self):
        return f"{self.cantidad} unidades {self.producto.producto}"

    def precio_unitario(self):
        return self.producto.precio 
        
    def sub_total(self):
        return self.producto.precio * self.cantidad