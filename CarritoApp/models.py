from django.db import models
from ElBuenSaborApp.models import Adicion, Producto
from django.db.models import F, Sum, FloatField

class Pedido(models.Model):
    # Eliminar el campo user
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

    def __str__(self):
        return str(self.id)
    
    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            total=Sum(F("producto__precio") * F("cantidad"), output_field=FloatField())
        )["total"]
    
class LineaPedido(models.Model):
    # Eliminar el campo user
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
