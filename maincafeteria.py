from cafeteria import *

productos = [
    Producto("Espresso", 35, 100),
    Producto("Capuchino", 55, 50),
    Producto("Muffin Vegano", 45, 15, es_vegano=True), 
    Producto("Brownie Sin Gluten", 50, 10, sin_gluten=True), 
    Producto("Latte Machiatto", 60, 45),
    Producto("Americano", 30, 100),
    Producto("Cuernito", 40, 20),
    Producto("Torta de tamal", 55, 10)
]
    

print("----------------- MENÚ CAFETERÍA MAX ------------------")

numero = 1
for p in productos:

    print(numero, "-", p.nombre, "$", p.precio)

    if p.es_vegano:
        print("   V")

    if p.sin_gluten:
        print("   SG")

    numero = numero + 1

opcion = int(input("\nElige un producto (1-8): ")) - 1
producto_elegido = productos[opcion]


control_suministros = Inventario()

if "Muffin" in producto_elegido.nombre or "Torta" in producto_elegido.nombre or "Cuernito" in producto_elegido.nombre:
    ingrediente = "Harina"
else:
    ingrediente = "Cafe"

if control_suministros.reducir_stock(ingrediente, 1):
    
    instrucciones = input("¿Instrucciones especiales?: ")
    desea_extra = input("¿Desea agregar un extra por $15? (si/no): ")
    precio_extra = 0
    if desea_extra.lower() == "si":
       precio_extra = 15

    
    empleado1 = Empleado(101, "Gabriela", "gabs@cafe.com", "E-500", "Barista")
    nombre_c = input("Tu nombre: ")
    correo_c = input("Tu correo: ")
    cliente1 = Persona(1, nombre_c, correo_c)
    pedido1 = Pedido(800, cliente1.nombre)
    
    if pedido1.agregar_producto(producto_elegido, instrucciones, precio_extra):
        
        
        empleado1.cambiar_estado_pedido(pedido1, "PREPARANDO")
        empleado1.cambiar_estado_pedido(pedido1, "ENTREGADO")

        
        print("\n----------------- TICKET DE VENTA ------------------")
        print("Atendido por:", empleado1.nombre)
        print("Cliente:", cliente1.nombre)
        print("Producto:", producto_elegido.nombre)
        print("Notas:", instrucciones)
        print("Total a pagar: $", pedido1.total)
        print("Estado final:", pedido1.estado)
        print("----------------------------------------------------")
        
    print("Suministros restantes de", ingrediente, ":", control_suministros.ingredientes[ingrediente])
else:
    print(f"No se puede preparar: falta {ingrediente} en inventario.")
    