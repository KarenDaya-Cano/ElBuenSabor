from django.db import models

class Producto(models.Model):
    producto = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.producto #return f'{self.producto} -> {self.precio}'

class Adicion(models.Model):
    adicion = models.CharField(max_length=50)
    precio = models.IntegerField()
    imagen = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'adicion'
        verbose_name_plural = 'adiciones'

    def __str__(self):
        return self.adicion
