from flask import Blueprint, request, jsonify
from ..services import socios as socios_service
from ..validators.socios import validar_datos_socios
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