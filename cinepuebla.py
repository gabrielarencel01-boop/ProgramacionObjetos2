class Pelicula:
    def __init__(self,titulo,duracion,clasificacion,genero):
        self.titulo=titulo
        self.duracion=duracion
        self.clasificacion=clasificacion
        self.genero=genero

class Sala:
    def __init__(self,tipo,capacidad_total,vip):
        self.tipo=tipo
        self.capacidad_total=capacidad_total
        self.vip=vip
        self.asientos_ocupados=[]

class Funcion:
    def __init__(self,id_funcion,horario_inicio,precio_base,pelicula,sala):
        self.id_funcion=id_funcion
        self.horario_inicio=horario_inicio
        self.precio_base=precio_base
        self.pelicula=pelicula
        self.sala=sala

class Promocion:
    def __init__(self,codigo,porcentaje_descuento):
        self.codigo=codigo
        self.porcentaje_descuento=porcentaje_descuento

    def aplicar_descuento(self,monto):
        return monto-(monto*self.porcentaje_descuento)
    
class Reserva:
    def __init__(self,id_reserva,funcion,monto_total):
        self.id_reserva=id_reserva
        self.funcion=funcion
        self.monto_total=monto_total
        self.estado="pensiente"
        self.asientos=[]

    def reservar_asientos(self,lista_asientos):
        print("Verificando disponibilidad")

        for asiento in lista_asientos:
            if asiento in self.funcion.sala.asientos_ocupados:
                print("El asiento",asiento,"ya eta ocupado")
                return False
        
        for asiento in lista_asientos:
            self.funcion.sala.asientos_ocupados.append(asiento)

        self.asientos=lista_asientos
        print("Asientos reservads con exito")
        return True
    
    def aplicar_promocion(self,promocion):
        self.monto_total=promocion.aplicar_descuento(self.monto_total)

    def confirmar_pago(self):
        self.estado="Pagado"

class Usuario:
    def __init__(self,id_usuario,nombre,gmail):
        self.id_usuario=id_usuario
        self.nombre=nombre
        self.gmail=gmail
        self.reservas=[]

    def agregar_reservas(self,reserva):
        self.reservas.append(reserva)
        
