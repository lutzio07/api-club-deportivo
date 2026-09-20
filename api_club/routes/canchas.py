from flask import Blueprint, jsonify, request

from ..services import canchas as canchas_service



canchas_bp = Blueprint('canchas', __name__)



@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():
    canchas = canchas_service.listar_canchas()

    return jsonify({"canchas": canchas})

@canchas_bp.route('/canchas', methods=['POST'])
def post_canchas():
    datos = request.get_json()
    nombre = datos["nombre"]
    id_deporte = datos["id_deporte"]
    precio_hora = datos["precio_hora"]
    techada = datos.get("techada", False)
    activa = datos.get("activa", True)

    nuevo_id = canchas_service.agregar_cancha(nombre,id_deporte,precio_hora,techada,activa)
    return "", 201
