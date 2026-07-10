from flask import Blueprint, request, jsonify
from controllers import category_controller
from middlewares.error_handler import AppError

category_bp = Blueprint('categories', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_categories_route():
    categories = category_controller.get_all_categories()
    return jsonify(categories), 200


@category_bp.route('/categories', methods=['POST'])
def create_category_route():
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    category, errors = category_controller.create_category(data)
    if errors:
        raise AppError(errors[0], 400)
    return jsonify(category.to_dict()), 201


@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category_route(cat_id):
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    category, errors = category_controller.update_category(cat_id, data)
    if errors:
        raise AppError(errors[0], 404)
    return jsonify(category.to_dict()), 200


@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category_route(cat_id):
    ok, error = category_controller.delete_category(cat_id)
    if not ok:
        raise AppError(error, 404)
    return jsonify({'message': 'Categoria deletada'}), 200
