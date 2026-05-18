from flask import Blueprint, request, jsonify
from services.task_service import TaskService

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = TaskService.get_all_tasks()
    result = []
    for t in tasks:
        d = t.to_dict()
        d['user_name'] = t.user.name if t.user else None
        d['category_name'] = t.category.name if t.category else None
        d['overdue'] = t.is_overdue()
        result.append(d)
    return jsonify(result), 200

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task = TaskService.create_task(data)
        return jsonify(task.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    data = TaskService.get_task_details(task_id)
    if data:
        return jsonify(data), 200
    return jsonify({'error': 'Task não encontrada'}), 404
