from flask import Blueprint, request, jsonify
from controllers import user_controller
from middlewares.error_handler import AppError

user_bp = Blueprint('users', __name__)


@user_bp.route('/users', methods=['GET'])
def get_users_route():
    users = user_controller.get_all_users()
    return jsonify(users), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise AppError('Usuário não encontrado', 404)
    data = user.to_dict()
    data['tasks'] = user_controller.get_user_tasks(user_id)
    return jsonify(data), 200


@user_bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    user, errors = user_controller.create_user(data)
    if errors:
        status = 409 if 'já cadastrado' in errors[0] else 400
        raise AppError(errors[0], status)
    return jsonify(user.to_dict()), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    user, errors = user_controller.update_user(user_id, data)
    if errors:
        status = 404 if 'não encontrado' in errors[0] else 409 if 'já cadastrado' in errors[0] else 400
        raise AppError(errors[0], status)
    return jsonify(user.to_dict()), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    ok, error = user_controller.delete_user(user_id)
    if not ok:
        raise AppError(error, 404)
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks_route(user_id):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise AppError('Usuário não encontrado', 404)
    tasks = user_controller.get_user_tasks(user_id)
    return jsonify(tasks), 200


@user_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    result, error = user_controller.login(data.get('email'), data.get('password'))
    if error:
        status = 400 if 'obrigatórios' in error else 401 if 'inválidas' in error else 403
        raise AppError(error, status)
    return jsonify(result), 200
