from api_club.repositories import canchas as canchas_repo


def listar_canchas():
    return canchas_repo.obtener_todas()

def agregar_cancha(nombre,id_deporte,precio_hora,techada,activa):
    return canchas_repo.crear_cancha(nombre,id_deporte,precio_hora,techada,activa)

def verificar_deporte(id_deporte):
    return canchas_repo.existe_deporte(id_deporte)