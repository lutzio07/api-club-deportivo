from flask import Blueprint, jsonify

from ..services import canchas as canchas_service



canchas_bp = Blueprint('canchas', __name__)



@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():
    canchas = canchas_service.listar_canchas()

    return jsonify({"canchas": canchas})