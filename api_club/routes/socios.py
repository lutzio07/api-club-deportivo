from flask import Blueprint, request, jsonify
from ..services import socios as socios_service
from ..validators.socios import (
    validar_datos_socios,
    validar_alta_socio,
    validar_actualizacion_socio,
)
socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():   
    limit = request.args.get('_limit', 10, type=int)
    offset = request.args.get('_offset', 0, type=int)
    nombre = request.args.get('nombre') 
    activo = request.args.get('activo')
    try:
        validar_datos_socios(limit, offset, nombre, activo) 
        socios = socios_service.get_socios(limit=limit, offset=offset, nombre=nombre, activo=activo)
        return jsonify(socios)
    except ValueError as xdd:
        return jsonify({"error": str(xdd)}), 400


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