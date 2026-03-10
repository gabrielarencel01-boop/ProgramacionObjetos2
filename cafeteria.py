class Persona:
    def __init__(self, id_persona, nombre, email):
        self.id_persona = id_persona
        self.nombre = nombre
        self.email = email
        self.puntos = 0

    def canjear_puntos(self, cantidad):
        if self.puntos >= cantidad:
            self.puntos -= cantidad
            print(f"Canje exitoso. Puntos restantes: {self.puntos}")
        else:
            print("Puntos insuficientes.")

class Inventario:
    def __init__(self):
        self.ingredientes = {"Cafe": 50, "Leche": 30, "Azucar": 20, "Harina": 40}

    def reducir_stock(self, nombre_ingrediente, cantidad):
        if nombre_ingrediente in self.ingredientes and self.ingredientes[nombre_ingrediente] >= cantidad:
            self.ingredientes[nombre_ingrediente] -= cantidad
            if self.ingredientes[nombre_ingrediente] < 5:
                print(f"--- ALERTA: Stock bajo de {nombre_ingrediente} ---")
            return True
        return False

class Empleado(Persona):
    def __init__(self, id_persona, nombre, email, id_empleado, rol):
        super().__init__(id_persona, nombre, email)
        self.id_empleado = id_empleado
        self.rol = rol 
        
    def cambiar_estado_pedido(self, pedido, nuevo_estado):
        pedido.estado = nuevo_estado
        print(f"Estado del pedido: {nuevo_estado}")

class Producto:
    def __init__(self, nombre, precio, stock, es_vegano=False, sin_gluten=False):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.es_vegano = es_vegano
        self.sin_gluten = sin_gluten

class Pedido:
    def __init__(self, id_pedido, cliente_nombre):
        self.id_pedido = id_pedido
        self.cliente_nombre = cliente_nombre
        self.items = []
        self.total = 0
        self.estado = "PENDIENTE"

    def agregar_producto(self, producto, personalizacion, precio_extra=0):
        if producto.stock > 0:
            self.items.append({"producto": producto.nombre, "nota": personalizacion})
            producto.stock -= 1
            self.total += (producto.precio + precio_extra)
            return True
        return False
    