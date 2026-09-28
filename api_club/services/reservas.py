from datetime import datetime
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