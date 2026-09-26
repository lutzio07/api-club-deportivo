from api_club.repositories import reservas as reservas_repo

def listar_reservas(limit, offset, id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    return reservas_repo.obtener_todas(
        limit, offset, id_cancha, id_socio, estado, fecha_desde, fecha_hasta
    )

def contar_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    return reservas_repo.contar_reservas(
        id_cancha, id_socio, estado, fecha_desde, fecha_hasta
    )