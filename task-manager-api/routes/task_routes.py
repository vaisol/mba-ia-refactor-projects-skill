from flask import Blueprint, request, jsonify
from controllers import task_controller
from middlewares.error_handler import AppError

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
def get_tasks_route():
    tasks = task_controller.get_all_tasks()
    return jsonify([t.to_dict() for t in tasks]), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_route(task_id):
    task = task_controller.get_task_by_id(task_id)
    if not task:
        raise AppError('Task não encontrada', 404)
    return jsonify(task.to_dict()), 200


@task_bp.route('/tasks', methods=['POST'])
def create_task_route():
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    task, errors = task_controller.create_task(data)
    if errors:
        raise AppError(errors[0], 400)
    return jsonify(task.to_dict()), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    data = request.get_json()
    if not data:
        raise AppError('Dados inválidos', 400)
    task, errors = task_controller.update_task(task_id, data)
    if errors:
        status = 404 if 'não encontrada' in errors[0].lower() else 400
        raise AppError(errors[0], status)
    return jsonify(task.to_dict()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    ok, error = task_controller.delete_task(task_id)
    if not ok:
        raise AppError(error, 404)
    return jsonify({'message': 'Task deletada com sucesso'}), 200


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks_route():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')
    tasks = task_controller.search_tasks(
        query=query or None,
        status=status or None,
        priority=priority or None,
        user_id=user_id or None
    )
    return jsonify([t.to_dict() for t in tasks]), 200


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats_route():
    stats = task_controller.get_task_stats()
    return jsonify(stats), 200
