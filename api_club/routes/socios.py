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

    parametros_permitidos = {"_limit", "_offset", "nombre", "activo"}

    parametros_desconocidos = set(request.args.keys()) - parametros_permitidos

    if parametros_desconocidos:
        return jsonify({
            "error": f"Parámetro(s) desconocido(s): {', '.join(parametros_desconocidos)}"
        }), 400

    limit = request.args.get('_limit')
    offset = request.args.get('_offset')

    if limit is None:
        limit = 10
    else:
        try:
            limit = int(limit)
        except ValueError:
            return jsonify({"error": "El parámetro _limit debe ser un número entero"}), 400

    if offset is None:
        offset = 0
    else:
        try:
            offset = int(offset)
        except ValueError:
            return jsonify({"error": "El parámetro _offset debe ser un número entero"}), 400
    nombre = request.args.get('nombre')
    activo = request.args.get('activo')

    if activo is not None:
        if activo.lower() == "true":
            activo = True
        elif activo.lower() == "false":
            activo = False
        else:
            return jsonify({"error": "El parámetro activo debe ser true o false"}), 400
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