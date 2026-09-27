from flask import Blueprint, request, jsonify
from urllib.parse import urlencode
from ..services import socios as socios_service
from ..utils import formatear_error
from ..validators.socios import (
    validar_datos_socios,
    validar_alta_socio,
    validar_actualizacion_socio,
)
socios_bp = Blueprint('socios', __name__)

PARAMETROS_PERMITIDOS = {"_limit", "_offset", "nombre", "activo"}

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    # Validación de parámetros
    desconocidos = set(request.args.keys()) - PARAMETROS_PERMITIDOS
    if desconocidos:    
        return jsonify(formatear_error("ERROR_VALIDACION", f"Parámetro(s) no permitido(s): {', '.join(desconocidos)}", "Error de validación")), 400
    # Paginación 
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        return jsonify(formatear_error("ERROR_VALIDACION", "Los parámetros _limit y _offset deben ser números enteros", "Error de validación")), 400
    # Filtros 
    nombre = request.args.get('nombre')
    activo_raw = request.args.get('activo')
    activo = None
    
    if activo_raw is not None:
        if activo_raw.lower() not in ["true", "false"]:
            return jsonify(formatear_error("ERROR_VALIDACION", "El parámetro activo debe ser true o false", "Error de validación")), 400
        activo = activo_raw.lower() == "true"
    
    try:
        validar_datos_socios(limit, offset, nombre, activo)
        socios, total = socios_service.get_socios(limit, offset, nombre, activo)
    except ValueError as e:
        return jsonify(formatear_error("ERROR_VALIDACION", str(e), "Error de validación")), 400

    # Armado HATEOAS 
    def crear_enlace(off):
        params = request.args.to_dict()
        params["_limit"] = limit
        params["_offset"] = off
        return f"{request.base_url}?{urlencode(params)}"

    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0
    prev_offset = (offset - limit) if offset >= limit else None
    next_offset = (offset + limit) if (offset + limit) < total else None

    enlaces = {
        "_first": {"href": crear_enlace(0)},
        "_prev": {"href": crear_enlace(prev_offset)} if prev_offset is not None else None,
        "_next": {"href": crear_enlace(next_offset)} if next_offset is not None else None,
        "_last": {"href": crear_enlace(last_offset)}
    }

    return jsonify({
        "socios": socios,
        "_links": enlaces
    }), 200
           
@socios_bp.route('/socios', methods=['POST'])
def post_socio():
    datos = request.get_json(silent=True)
    try:
        datos_validados = validar_alta_socio(datos)
    except ValueError as xdd:
        return jsonify({"error": str(xdd)}), 400

    socio, motivo = socios_service.crear_socio(
        datos_validados["nombre"], datos_validados["email"]
    )

    if motivo == "EMAIL_DUPLICADO":
        return jsonify({"error": "Ya existe un socio registrado con ese email"}), 409

    return jsonify(socio), 201


@socios_bp.route('/socios/<id_socio>', methods=['GET'])
def get_socio(id_socio):
    try:
        id_socio = int(id_socio)
    except ValueError:
        return jsonify({"error": "El ID debe ser un número entero"}), 400

    socio = socios_service.obtener_socio_por_id(id_socio)

    if not socio:
        return jsonify({"error": "No se encontró un socio con el ID indicado"}), 404

    return jsonify(socio)


@socios_bp.route('/socios/<id_socio>', methods=['PATCH'])
def patch_socio(id_socio):
    try:
        id_socio = int(id_socio)
    except ValueError:
        return jsonify({"error": "El ID debe ser un número entero"}), 400

    datos = request.get_json(silent=True)
    try:
        campos_validados = validar_actualizacion_socio(datos)
    except ValueError as xdd:
        return jsonify({"error": str(xdd)}), 400

    socio, motivo = socios_service.actualizar_socio(id_socio, campos_validados)

    if motivo == "NO_ENCONTRADO":
        return jsonify({"error": "No se encontró un socio con el ID indicado"}), 404

    if motivo == "EMAIL_DUPLICADO":
        return jsonify({"error": "Ya existe un socio registrado con ese email"}), 409

    return jsonify(socio)