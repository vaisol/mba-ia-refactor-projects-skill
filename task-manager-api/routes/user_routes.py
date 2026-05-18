from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = UserService.get_all_users()
        result = []
        for u in users:
            user_data = u.to_dict()
            user_data['task_count'] = len(u.tasks)
            result.append(user_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = UserService.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao criar usuário', 'details': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    try:
        user = UserService.update_user(user_id, data)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar', 'details': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        success = UserService.delete_user(user_id)
        if not success:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao deletar', 'details': str(e)}), 500

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

        result = []
        for t in user.tasks:
            task_data = t.to_dict()
            task_data['overdue'] = t.is_overdue()
            result.append(task_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    email = data.get('email')
    password = data.get('password')

    try:
        user = UserService.login(email, password)
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Erro no login', 'details': str(e)}), 500
