from flask import Blueprint, jsonify, request
from urllib.parse import urlencode

from ..services import canchas as canchas_service
from ..validators import canchas as canchas_validator


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
        "_first": crear_enlace(first_offset),
        "_prev": crear_enlace(prev_offset) if prev_offset is not None else None,
        "_next": crear_enlace(next_offset) if next_offset is not None else None,
        "_last": crear_enlace(last_offset)
    }

    return jsonify({
        "canchas": canchas,
        **enlaces
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