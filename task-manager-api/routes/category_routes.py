from flask import Blueprint, request, jsonify
from services.category_service import CategoryService

category_bp = Blueprint('categories', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = CategoryService.get_all_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        category = CategoryService.create_category(data)
        return jsonify(category.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao criar categoria', 'details': str(e)}), 500

@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    data = request.get_json()
    try:
        cat = CategoryService.update_category(cat_id, data)
        if not cat:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        return jsonify(cat.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar', 'details': str(e)}), 500

@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    try:
        success = CategoryService.delete_category(cat_id)
        if not success:
            return jsonify({'error': 'Categoria não encontrada'}), 404
        return jsonify({'message': 'Categoria deletada'}), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar', 'details': str(e)}), 500
