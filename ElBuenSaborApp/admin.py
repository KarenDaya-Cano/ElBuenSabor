from django.contrib import admin
from ElBuenSaborApp.models import Producto, Adicion

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Producto, ProductoAdmin)

class AdicionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Adicion, AdicionAdmin)
