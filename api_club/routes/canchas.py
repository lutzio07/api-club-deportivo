from flask import Blueprint, jsonify, request

from ..services import canchas as canchas_service



canchas_bp = Blueprint('canchas', __name__)



@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():
    canchas = canchas_service.listar_canchas()

    return jsonify({"canchas": canchas})

@canchas_bp.route('/canchas', methods=['POST'])
def post_canchas():
    datos = request.get_json(silent=True)

    if not isinstance(datos,dict):
        return jsonify({"errors": [{
                    "code": "ERROR_VALIDACION",
                    "message": "El cuerpo de la solicitud no es valido.",
                    "level": "error",
                    "description": "El cuerpo de la solicitud debe ser un JSON valido."
                }]}), 400

    if "nombre" not in datos:
        return jsonify({"errors": [{
            "code": "ERROR_VALIDACION",
            "message": "El cuerpo de la solicitud no es valido.",
            "level": "error",
            "description": "El campo 'nombre' es obligatorio"
        }]}), 400

    if "id_deporte" not in datos:
        return jsonify({"errors": [{
            "code": "ERROR_VALIDACION",
            "message": "El cuerpo de la solicitud no es valido.",
            "level": "error",
            "description": "El campo 'id_deporte' es obligatorio"
        }]}), 400
    
    if "precio_hora" not in datos:
        return jsonify({"errors": [{
            "code": "ERROR_VALIDACION",
            "message": "El cuerpo de la solicitud no es valido.",
            "level": "error",
            "description": "El campo 'precio_hora' es obligatorio"
        }]}), 400

    
    nombre = datos["nombre"]
    id_deporte = datos["id_deporte"]
    precio_hora = datos["precio_hora"]
    techada = datos.get("techada", False)
    activa = datos.get("activa", True)

    if not isinstance(nombre,str):
        return jsonify({"errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud no es valido.",
                "level": "error",
                "description": "El campo  'nombre' debe ser de tipo string."
        }]}), 400

    if not isinstance(id_deporte,int) or isinstance(id_deporte,bool):
        return jsonify({"errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud no es valido.",
                "level": "error",
                "description": "El campo 'id_deporte' debe ser de tipo entero."
        }]}), 400

    if not isinstance(precio_hora,int) or isinstance(precio_hora,bool):
        return jsonify({"errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud no es valido.",
                "level": "error",
                "description": "El campo 'precio_hora' debe ser de tipo entero."
        }]}), 400

    if precio_hora <= 0:
            return jsonify({"errors": [{
                    "code": "ERROR_VALIDACION",
                    "message": "El cuerpo de la solicitud no es valido.",
                    "level": "error",
                    "description": "El campo 'precio_hora' debe ser mayor a cero."
            }]}), 400
    
    if not isinstance(techada,bool):
        return jsonify({"errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud no es valido.",
                "level": "error",
                "description": "El campo 'techada' debe ser de tipo bool."
        }]}), 400

    if not isinstance(activa,bool):
        return jsonify({"errors": [{
                "code": "ERROR_VALIDACION",
                "message": "El cuerpo de la solicitud no es valido.",
                "level": "error",
                "description": "El campo 'activa' debe ser de tipo bool."
        }]}), 400

    if not canchas_service.verificar_deporte(id_deporte):
        return jsonify({"errors": [{
                "code": "DEPORTE_NO_ENCONTRADO",
                "message": "El recurso no se encontro",
                "level": "error",
                "description": "El campo 'id_deporte' no corresponde a ningun deporte existente."
        }]}), 404
    
    nuevo_id = canchas_service.agregar_cancha(nombre,id_deporte,precio_hora,techada,activa)
    return "", 201
