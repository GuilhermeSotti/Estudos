from flask import Blueprint, request, jsonify
from models import Plantio, Insumo

plantio_bp = Blueprint('plantio', __name__)

@plantio_bp.route('/calcular_metricas', methods=['POST'])
def calcular_metricas():
    data = request.get_json()
    plantio_id = data.get('plantio_id')
    plantio = Plantio.query.get(plantio_id)
    
    if not plantio:
        return jsonify({'error': 'Plantio não encontrado'}), 404

    # Exemplo de cálculo de métricas
    area_total = plantio.area
    produtividade = plantio.producao / area_total

    return jsonify({
        'area_total': area_total,
        'produtividade': produtividade
    })

@plantio_bp.route('/calcular_insumos', methods=['POST'])
def calcular_insumos():
    data = request.get_json()
    plantio_id = data.get('plantio_id')
    plantio = Plantio.query.get(plantio_id)
    
    if not plantio:
        return jsonify({'error': 'Plantio não encontrado'}), 404

    # Exemplo de cálculo de insumos
    insumos = Insumo.query.filter_by(plantio_id=plantio_id).all()
    total_insumos = sum(insumo.quantidade for insumo in insumos)

    return jsonify({
        'total_insumos': total_insumos
    })