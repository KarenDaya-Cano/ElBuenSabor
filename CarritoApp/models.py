from django.db import models
from ElBuenSaborApp.models import Adicion, Producto
from django.db.models import F, Sum, DecimalField

class Pedido(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['created']  # Ordenar por fecha de creación

    def __str__(self):
        return str(self.id)
    
    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            total=Sum(F("producto__precio") * F("cantidad"), output_field=DecimalField())
        )["total"] or 0  # Valor por defecto de 0 si no hay ítems de línea

class LineaPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    adiciones = models.ManyToManyField(Adicion, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lineapedido'
        verbose_name = 'línea pedido'
        verbose_name_plural = 'líneas pedidos'

    def __str__(self):
        return f"{self.cantidad} unidades {self.producto.producto}"

    def precio_unitario(self):
        return self.producto.precio 
        
    def sub_total(self):
        return self.producto.precio * self.cantidad
