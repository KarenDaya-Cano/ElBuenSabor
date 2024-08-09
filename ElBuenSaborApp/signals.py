import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Producto, Adicion

@receiver(post_delete, sender=Producto)
def delete_producto_image(sender, instance, **kwargs):
    # Verifica si el archivo existe antes de intentar eliminarlo
    if instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)

@receiver(post_delete, sender=Adicion)
def delete_adicion_image(sender, instance, **kwargs):
    # Verifica si el archivo existe antes de intentar eliminarlo
    if instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)