from api_club.repositories import canchas as canchas_repo


def listar_canchas(limit, offset, nombre=None, id_deporte=None, techada=None, activa=None):
    return canchas_repo.obtener_todas(
        limit,
        offset,
        nombre,
        id_deporte,
        techada,
        activa
    )

def contar_canchas(nombre=None, id_deporte=None, techada=None, activa=None):
    return canchas_repo.contar_canchas(
        nombre,
        id_deporte,
        techada,
        activa
    )

def crear_cancha(nombre, id_deporte, precio_hora, techada, activa):

    existe = canchas_repo.existe_deporte(id_deporte)

    if not existe:
        return None, "El deporte indicado no existe"

    id_nueva = canchas_repo.crear_cancha(
        nombre,
        id_deporte,
        precio_hora,
        techada,
        activa
    )

    return id_nueva, None