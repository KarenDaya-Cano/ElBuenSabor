class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.carrito = self.session.get("carrito", {})

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito: # quite el key()
            self.carrito[id] = {
                "producto_id": producto.id,
                "producto": producto.producto,
                "precio": producto.precio,
                "descripcion": producto.descripcion,
                "imagen": producto.imagen.url,
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["precio"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito: #quite el .keys()
            self.carrito[producto_id]["cantidad"] -= 1
            self.carrito[producto_id]["precio"] -= producto.precio  # Restar el precio del producto
            if self.carrito[producto_id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.guardar_carrito()
