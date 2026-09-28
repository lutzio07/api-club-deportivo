from datetime import datetime, timedelta, timezone
from api_club.repositories import reservas as reservas_repo
from api_club.repositories import canchas as canchas_repo
from api_club.repositories import socios as socios_repo

def listar_reservas(limit, offset, id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    return reservas_repo.obtener_todas(
        limit, offset, id_cancha, id_socio, estado, fecha_desde, fecha_hasta
    )

def contar_reservas(id_cancha=None, id_socio=None, estado=None, fecha_desde=None, fecha_hasta=None):
    return reservas_repo.contar_reservas(
        id_cancha, id_socio, estado, fecha_desde, fecha_hasta
    )

def crear_reserva(datos):
    id_socio = datos["id_socio"]
    id_cancha = datos["id_cancha"]
    fecha_hora_inicio = datos["fecha_hora_inicio"]
    fecha_hora_fin = datos["fecha_hora_fin"]

    socio = socios_repo.obtener_por_id(id_socio)
    if not socio:
        return None, ("ERROR_NO_ENCONTRADO", "Socio no encontrado", 404)
    if not socio["activo"]:
        return None, ("ERROR_CONFLICTO", "El socio está inactivo", 409)
    cancha = canchas_repo.obtener_datos_cancha(id_cancha)
    if not cancha:
        return None, ("ERROR_NO_ENCONTRADO", "Cancha no encontrada", 404)
    if not cancha["activa"]:
        return None, ("ERROR_CONFLICTO", "La cancha está inactiva", 409)

    inicio = datetime.strptime(fecha_hora_inicio, "%Y-%m-%dT%H:%M:%S.%f-03:00")
    fin = datetime.strptime(fecha_hora_fin, "%Y-%m-%dT%H:%M:%S.%f-03:00")
    if inicio.date() != fin.date():
        return None, ("ERROR_VALIDACION", "La reserva debe empezar y terminar el mismo día", 400)
    if inicio >= fin:
        return None, ("ERROR_VALIDACION", "La hora de inicio debe ser anterior a la hora de fin", 400)
    if inicio.minute != 0 or inicio.second != 0 or fin.minute != 0 or fin.second != 0:
        return None, ("ERROR_VALIDACION", "Las horas deben ser exactas (en punto)", 400)
    ahora = datetime.now()
    if inicio <= ahora:
        return None, ("ERROR_VALIDACION", "No se puede reservar en el pasado", 400)

    if reservas_repo.hay_superposicion_cancha(id_cancha, fecha_hora_inicio, fecha_hora_fin):
        return None, ("ERROR_CONFLICTO", "La cancha ya tiene una reserva en ese horario", 409)
    if reservas_repo.hay_superposicion_socio(id_socio, fecha_hora_inicio, fecha_hora_fin):
        return None, ("ERROR_CONFLICTO", "El socio ya tiene una reserva en ese horario", 409)

    horas = (fin - inicio).seconds // 3600
    precio_hora = cancha["precio_hora"]
    precio_total = precio_hora * horas
    id_nueva = reservas_repo.crear_reserva(
        id_socio, 
        id_cancha,
        fecha_hora_inicio, 
        fecha_hora_fin,
        precio_hora, 
        precio_total
    )

    return id_nueva, None

def obtener_reserva_por_id(id_reserva):
    return reservas_repo.obtener_reserva_por_id(id_reserva)

def modificar_estado_reserva(id_reserva, estado_solicitado):
    estados_permitidos = {"confirmada", "cancelada", "finalizada"}
    if estado_solicitado not in estados_permitidos:
        return None, (
            "ERROR_VALIDACION",
            "Estado inválido",
            400
        )

    reserva = reservas_repo.obtener_reserva_por_id(id_reserva)
    if not reserva:
        return None, (
            "ERROR_NO_ENCONTRADO",
            "Reserva no encontrada",
            404
        )

    if reserva["estado"] == estado_solicitado:
        return reserva, None

    if reserva["estado"] != "confirmada":
        return None, (
            "ERROR_CONFLICTO",
            "No se permite cambiar el estado de una reserva terminal",
            409
        )

    ahora_gmt_menos_3 = datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None)

    if estado_solicitado == "cancelada":
        if ahora_gmt_menos_3 >= reserva["fecha_hora_inicio"]:
            return None, (
                "ERROR_CONFLICTO",
                "La reserva solo puede cancelarse antes de su hora de inicio",
                409
            )
    elif estado_solicitado == "finalizada":
        if ahora_gmt_menos_3 < reserva["fecha_hora_fin"]:
            return None, (
                "ERROR_CONFLICTO",
                "La reserva solo puede finalizarse al alcanzar su hora de fin",
                409
            )

    actualizada = reservas_repo.actualizar_estado_reserva(id_reserva, estado_solicitado)
    if actualizada:
        return reservas_repo.obtener_reserva_por_id(id_reserva), None

    reserva_actual = reservas_repo.obtener_reserva_por_id(id_reserva)
    if not reserva_actual:
        return None, (
            "ERROR_NO_ENCONTRADO",
            "Reserva no encontrada",
            404
        )
    if reserva_actual["estado"] == estado_solicitado:
        return reserva_actual, None

    return None, (
        "ERROR_CONFLICTO",
        "La reserva cambió mientras se procesaba la solicitud",
        409
    )