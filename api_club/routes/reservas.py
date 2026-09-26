from flask import Blueprint, request, jsonify
from urllib.parse import urlencode
from api_club.utils import formatear_error
from api_club.validators import reservas as reservas_validator
from api_club.services import reservas as reservas_service

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def get_reservas():

    parametros_permitidos = {
        '_limit',
        '_offset',
        'id_cancha',
        'id_socio',
        'estado',
        'fecha_desde',
        'fecha_hasta'
    }
    
    parametros_recibidos = set(request.args.keys())
    
    parametros_desconocidos = parametros_recibidos - parametros_permitidos
    
    if parametros_desconocidos:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Parámetro(s) desconocido(s)",
            f"Los siguientes parámetros no están permitidos: {', '.join(parametros_desconocidos)}"
        )), 400

    limit = request.args.get('_limit')
    offset = request.args.get('_offset')
    id_cancha = request.args.get('id_cancha')
    id_socio = request.args.get('id_socio')
    estado = request.args.get('estado')
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')

    error_paginacion = reservas_validator.validar_paginacion(limit, offset)
    if error_paginacion:
        return jsonify(formatear_error(
            "ERROR_VALIDACION", 
            "Paginación inválida", 
            error_paginacion
        )), 400

    error_filtros = reservas_validator.validar_filtros_reservas(id_cancha, id_socio, estado, fecha_desde, fecha_hasta)
    if error_filtros:
        return jsonify(formatear_error(
            "ERROR_VALIDACION", 
            "Filtros inválidos", 
            error_filtros
        )), 400

    limit_int = int(limit) if limit else 10
    offset_int = int(offset) if offset else 0

    reservas = reservas_service.listar_reservas(
        limit=limit_int, 
        offset=offset_int, 
        id_cancha=id_cancha, 
        id_socio=id_socio, 
        estado=estado, 
        fecha_desde=fecha_desde, 
        fecha_hasta=fecha_hasta
    )

    if not reservas:
        return '', 204

    total = reservas_service.contar_reservas(
        id_cancha=id_cancha, id_socio=id_socio, 
        estado=estado, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
    )
    first_offset = 0
    last_offset = ((total - 1) // limit_int) * limit_int if total > 0 else 0
    prev_offset = offset_int - limit_int if offset_int >= limit_int else None
    next_offset = offset_int + limit_int if offset_int + limit_int < total else None

    def crear_enlace(nuevo_offset):
        parametros = request.args.to_dict()
        parametros["_offset"] = nuevo_offset
        return f"{request.base_url}?{urlencode(parametros)}"

    enlaces = {
        "_first": crear_enlace(first_offset),
        "_prev": crear_enlace(prev_offset) if prev_offset is not None else None,
        "_next": crear_enlace(next_offset) if next_offset is not None else None,
        "_last": crear_enlace(last_offset)
    }

    return jsonify({
        "reservas": reservas,
        "_links": enlaces
    }), 200