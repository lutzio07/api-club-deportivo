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

@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():

    datos = request.get_json()
    error_validacion = reservas_validator.validar_creacion_reserva(datos)

    if error_validacion:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Datos invalidos",
            error_validacion
        )), 400

    resultado, error = reservas_service.crear_reserva(datos)
    
    if error:
        codigo, mensaje, status = error
        return jsonify(formatear_error(codigo, mensaje, mensaje)), status
    return '', 201

@reservas_bp.route('/reservas/<id_reserva>', methods=['GET'])
def get_reserva(id_reserva):
    error_reserva = reservas_validator.validar_id_reserva(id_reserva)
    if error_reserva:
        return error_reserva

    reserva = reservas_service.obtener_reserva_por_id(id_reserva)
    if not reserva:
        return jsonify(formatear_error(
            "ERROR_NO_ENCONTRADO",
            "Reserva no encontrada",
            "No se encontro una reserva con el id indicado"
        )), 404

    return jsonify(reserva), 200

@reservas_bp.route('/reservas/<id_reserva>/estado', methods=['PUT'])
def put_estado_reserva(id_reserva):
    error_id = reservas_validator.validar_id_reserva(id_reserva)
    if error_id:
        return error_id

    id_reserva = int(id_reserva)
    datos = request.get_json(silent=True)
    error_validacion = reservas_validator.validar_actualizacion_estado_reserva(datos)

    if error_validacion:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Estado inválido",
            error_validacion
        )), 400

    reserva, error = reservas_service.modificar_estado_reserva(
        id_reserva,
        datos["estado"]
    )

    if error:
        codigo, mensaje, status = error
        return jsonify(formatear_error(codigo, mensaje, mensaje)), status

    return jsonify(reserva), 200