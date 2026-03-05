from cinepuebla import*

print("Peliculas disponibles")
Peliculas = [
    Pelicula("Avenger", 120, "A", "Accion"),
    Pelicula("Mario Bross", 100, "A", "Animacion"),
    Pelicula("Titanic", 195, "B", "Romance"),
    Pelicula("Batman", 130, "B ", "Accion"),
    Pelicula("Coco", 105, "A", "Animacion"),
    Pelicula("Spiderman", 125, "A", "Accion"),
    Pelicula("Frozen", 102, "A", "Infantil"),
    Pelicula("Joker", 122, "C", "Drama"),
    Pelicula("Rapidos y Furiosos", 140, "B", "Accion"),
    Pelicula("El Conjuro", 110, "C", "Terror")
    ]

for i in range(len(Peliculas)):
    print(i+1,Peliculas[i].titulo)

print("Compra de boletos")
opcion=int(input("Elige tu pelicula(1-10):"))-1

sala1=Sala("Normal",100,False)
funcion_seleccionada=Funcion(1,"18:00",150,Peliculas[opcion],sala1)

nombre=input("Nombre:")
correo=input("Correo:")

usuario1=Usuario(1,nombre,correo)
reserva1=Reserva(1,funcion_seleccionada,funcion_seleccionada.precio_base)

asientos=input("Elija sus asientos(A1,A2):").split(",")

if reserva1.reservar_asientos(asientos):
    usar_promo=input("Tienes codigo de descuento?(si/no):")
    if usar_promo.lower() == "si":
        codigo=input("Ingresa el codigo:")

        if codigo=="PROMO10":
            promo=Promocion("PROMO10",0.10)
            reserva1.aplicar_promocion(promo)
            print("Se aplico 10% de descuento")

        elif codigo=="PROMO20":
            promo=Promocion("PROMO20",0.20)
            reserva1.aplicar_promocion(promo)
            print("Se aplico 20% de descuento")

        elif codigo=="VIP30":
            promo=Promocion("VIP30",0.30)
            reserva1.aplicar_promocion(promo)
            print("Se aplico 30% de descuento")

        else:
            print("Codigo incorrecto, no se aplico el descuento")

reserva1.confirmar_pago()
print("Pago confirmado")

usuario1.agregar_reservas(reserva1)
print("Reserva agregada al usuario")
print("Resumen de compra")
print("Usuario:",usuario1.nombre)
print("Pelicula:",reserva1.funcion.pelicula.titulo)
print("Asientos:",reserva1.asientos)
print("Total:",reserva1.monto_total)
print("Estado:",reserva1.estado)



