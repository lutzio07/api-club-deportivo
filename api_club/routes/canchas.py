from flask import Blueprint, jsonify, request
from urllib.parse import urlencode

from ..services import canchas as canchas_service
from ..validators import canchas as canchas_validator
from ..utils import formatear_error


canchas_bp = Blueprint('canchas', __name__)


@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():

    parametros_permitidos = {
        '_limit',
        '_offset',
        'nombre',
        'id_deporte',
        'techada',
        'activa'
    }

    parametros_recibidos = set(request.args.keys())

    parametros_desconocidos = parametros_recibidos - parametros_permitidos

    if parametros_desconocidos:
        return jsonify({
            "error": "Parámetro(s) desconocido(s)",
            "parametros": list(parametros_desconocidos)
        }), 400


    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        return jsonify({"error": "Los parámetros _limit y _offset deben ser números enteros"}), 400

    if limit < 1 or limit > 100:
        return jsonify({"error": "_limit debe estar entre 1 y 100"}), 400

    if offset < 0:
        return jsonify({"error": "_offset no puede ser negativo"}), 400

    nombre = request.args.get('nombre')

    try:
        id_deporte = int(request.args.get('id_deporte')) if request.args.get('id_deporte') is not None else None
    except ValueError:
        return jsonify({"error": "id_deporte debe ser un número entero"}), 400

    if id_deporte is not None and id_deporte < 1:
        return jsonify({"error": "id_deporte debe ser un número positivo"}), 400

    techada_param = request.args.get('techada')

    if techada_param is not None:
        if techada_param == 'true':
            techada = True
        elif techada_param == 'false':
            techada = False
        else:
            return jsonify({"error": "techada debe ser true o false"}), 400
    else:
        techada = None

    activa_param = request.args.get('activa')

    if activa_param is not None:
        if activa_param == 'true':
            activa = True
        elif activa_param == 'false':
            activa = False
        else:
            return jsonify({"error": "activa debe ser true o false"}), 400
    else:
        activa = None

    canchas = canchas_service.listar_canchas(
        limit,
        offset,
        nombre,
        id_deporte,
        techada,
        activa
    )

    total = canchas_service.contar_canchas(
        nombre,
        id_deporte,
        techada,
        activa
    )

    if not canchas:
        return '', 204

    # Calcular las posiciones de las páginas
    first_offset = 0

    if total > 0:
        last_offset = ((total - 1) // limit) * limit
    else:
        last_offset = 0

    if offset >= limit:
        prev_offset = offset - limit
    else:
        prev_offset = None

    if offset + limit < total:
        next_offset = offset + limit
    else:
        next_offset = None

    def crear_enlace(nuevo_offset):
        parametros = request.args.to_dict()
        parametros["_offset"] = nuevo_offset

        return f"{request.base_url}?{urlencode(parametros)}"

    enlaces = {
        "_first": {"href": crear_enlace(first_offset)},
        "_prev": {"href": crear_enlace(prev_offset)} if prev_offset is not None else None,
        "_next": {"href": crear_enlace(next_offset)} if next_offset is not None else None,
        "_last": {"href": crear_enlace(last_offset)}
    }

    return jsonify({
        "canchas": canchas,
        "_links": enlaces
    })


@canchas_bp.route('/canchas', methods=['POST'])
def crear_cancha():

    datos = request.get_json()

    error = canchas_validator.validar_datos_cancha(datos)

    if error:
        return jsonify({"error": error}), 400

    id_nueva, error = canchas_service.crear_cancha(
        datos['nombre'],
        datos['id_deporte'],
        datos['precio_hora'],
        datos['techada'],
        datos['activa']
    )

    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "id": id_nueva,
        "nombre": datos['nombre'],
        "id_deporte": datos['id_deporte'],
        "precio_hora": datos['precio_hora'],
        "techada": datos['techada'],
        "activa": datos['activa']
    }), 201

@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def consultar_disponibilidad():

    parametros_permitidos = {
        "fecha",
        "hora_inicio",
        "hora_fin",
        "id_deporte",
        "techada",
        "_limit",
        "_offset"
    }

    parametros_recibidos = set(request.args.keys())

    parametros_desconocidos = parametros_recibidos - parametros_permitidos

    if parametros_desconocidos:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Parámetro(s) desconocido(s)",
            f"Los siguientes parámetros no están permitidos: {', '.join(parametros_desconocidos)}"
        )), 400

    fecha = request.args.get("fecha")
    hora_inicio = request.args.get("hora_inicio")
    hora_fin = request.args.get("hora_fin")

    id_deporte = request.args.get("id_deporte")
    techada = request.args.get("techada")

    limit = request.args.get("_limit", default="10")
    offset = request.args.get("_offset", default="0")

    if id_deporte is not None:
        try:
            id_deporte = int(id_deporte)
        except ValueError:
            return jsonify(formatear_error(
                "ERROR_VALIDACION",
                "Parámetro id_deporte inválido",
                "id_deporte debe ser un número entero."
            )), 400

    if techada is not None:
        if techada == "true":
            techada = True
        elif techada == "false":
            techada = False
        else:
            return jsonify(formatear_error(
                "ERROR_VALIDACION",
                "Parámetro techada inválido",
                "techada debe ser true o false."
            )), 400

    try:
        limit = int(limit)
        offset = int(offset)
    except ValueError:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Parámetros de paginación inválidos",
            "_limit y _offset deben ser números enteros."
        )), 400

    error = canchas_validator.validar_parametros_disponibilidad(
        fecha,
        hora_inicio,
        hora_fin
    )

    if error:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Parámetros de disponibilidad inválidos",
            error
        )), 400

    error = canchas_validator.validar_filtros_disponibilidad(
        id_deporte,
        techada
    )

    if error:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Filtros de disponibilidad inválidos",
            error
        )), 400

    error = canchas_validator.validar_paginacion(
        limit,
        offset
    )

    if error:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Parámetros de paginación inválidos",
            error
        )), 400

    canchas = canchas_service.consultar_disponibilidad(
        fecha,
        hora_inicio,
        hora_fin,
        id_deporte,
        techada,
        limit,
        offset
    )

    total = canchas_service.contar_disponibles(
        fecha,
        hora_inicio,
        hora_fin,
        id_deporte,
        techada
    )
    if not canchas:
        return '', 204

    first_offset = 0

    if total > 0:
        last_offset = ((total - 1) // limit) * limit
    else:
        last_offset = 0

    if offset >= limit:
        prev_offset = offset - limit
    else:
        prev_offset = None

    if offset + limit < total:
        next_offset = offset + limit
    else:
        next_offset = None

    def crear_enlace(nuevo_offset):
        parametros = request.args.to_dict()
        parametros["_offset"] = nuevo_offset

        return f"{request.base_url}?{urlencode(parametros)}"

    enlaces = {
        "_first": {"href": crear_enlace(first_offset)},
        "_prev": {"href": crear_enlace(prev_offset)} if prev_offset is not None else None,
        "_next": {"href": crear_enlace(next_offset)} if next_offset is not None else None,
        "_last": {"href": crear_enlace(last_offset)}
    }

    return jsonify({
        "canchas": canchas,
        "_links": enlaces
    })

@canchas_bp.route('/canchas/<id_cancha>', methods=['GET'])
def obtener_cancha(id_cancha):
    try:
        id_cancha = int(id_cancha)
    except ValueError:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número entero."
        )), 400

    if id_cancha < 1:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número positivo."
        )), 400

    cancha = canchas_service.obtener_cancha_por_id(id_cancha)

    if not cancha:
        return jsonify(formatear_error(
            "ERROR_NO_ENCONTRADO",
            "Cancha no encontrada",
            "No se encontró una cancha con el ID indicado."
        )), 404

    return jsonify(cancha), 200

@canchas_bp.route('/canchas/<id_cancha>', methods=['PATCH'])
def actualizar_cancha(id_cancha):

    try:
        id_cancha = int(id_cancha)
    except ValueError:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número entero."
        )), 400

    if id_cancha < 1:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número positivo."
        )), 400

    datos = request.get_json(silent=True)

    error = canchas_validator.validar_datos_actualizacion_cancha(datos)

    if error:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "Datos de actualización inválidos",
            error
        )), 400

    actualizado = canchas_service.actualizar_cancha(
        id_cancha,
        datos
    )

    if not actualizado:
        return jsonify(formatear_error(
            "ERROR_NO_ENCONTRADO",
            "Cancha no encontrada",
            "No se encontró una cancha con el ID indicado."
        )), 404

    return '', 204

@canchas_bp.route('/canchas/<id_cancha>', methods=['DELETE'])
def eliminar_cancha(id_cancha):

    try:
        id_cancha = int(id_cancha)
    except ValueError:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número entero."
        )), 400

    if id_cancha < 1:
        return jsonify(formatear_error(
            "ERROR_VALIDACION",
            "El ID no es válido",
            "El ID debe ser un número positivo."
        )), 400

    eliminado, motivo = canchas_service.eliminar_cancha(id_cancha)

    if not eliminado:

        if motivo == "NO_ENCONTRADA":
            return jsonify(formatear_error(
                "ERROR_NO_ENCONTRADO",
                "Cancha no encontrada",
                "No se encontró una cancha con el ID indicado."
            )), 404

        if motivo == "TIENE_RESERVAS":
            return jsonify(formatear_error(
                "ERROR_CONFLICTO",
                "No se puede eliminar la cancha",
                "La cancha tiene reservas asociadas."
            )), 409

    return '', 204