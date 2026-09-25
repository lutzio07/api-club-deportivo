from api_club.repositories import canchas as canchas_repo
# listar canchas con filtros y paginación

def listar_canchas(limit, offset, nombre=None, id_deporte=None, techada=None, activa=None):
    return canchas_repo.obtener_todas(
        limit,
        offset,
        nombre,
        id_deporte,
        techada,
        activa
    )

# contar el total de canchas con filtros

def contar_canchas(nombre=None, id_deporte=None, techada=None, activa=None):
    return canchas_repo.contar_canchas(
        nombre,
        id_deporte,
        techada,
        activa
    )
# crear una nueva cancha

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

# obtener los datos de una cancha por su ID

def obtener_cancha_por_id(id_cancha):
    return canchas_repo.obtener_datos_cancha(id_cancha)

def actualizar_cancha(id_cancha, datos):

    cancha = canchas_repo.obtener_datos_cancha(id_cancha)

    if not cancha:
        return False

    canchas_repo.actualizar_cancha(id_cancha, datos)

    return True

def eliminar_cancha(id_cancha):

    cancha = canchas_repo.obtener_datos_cancha(id_cancha)

    if not cancha:
        return False, "NO_ENCONTRADA"

    if canchas_repo.tiene_reservas(id_cancha):
        return False, "TIENE_RESERVAS"

    canchas_repo.eliminar_cancha(id_cancha)

    return True, None

def consultar_disponibilidad(
    fecha,
    hora_inicio,
    hora_fin,
    id_deporte=None,
    techada=None,
    limit=10,
    offset=0
):
    return canchas_repo.obtener_disponibles(
        fecha,
        hora_inicio,
        hora_fin,
        id_deporte,
        techada,
        limit,
        offset
    )

def contar_disponibles(
    fecha,
    hora_inicio,
    hora_fin,
    id_deporte=None,
    techada=None
):
    return canchas_repo.contar_disponibles(
        fecha,
        hora_inicio,
        hora_fin,
        id_deporte,
        techada
    )