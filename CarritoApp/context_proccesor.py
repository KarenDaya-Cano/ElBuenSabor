def total_carrito(request):
    total = 0 
    carro = request.session.get('carrito',{})
    for key, value in carro.items():
        total += int(value["precio"])
    return {"total_carrito": total}