from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime


def get_all_tasks():
    return Task.query.all()


def get_task_by_id(task_id):
    return Task.query.get(task_id)


def create_task(data):
    errors = validate_task_data(data)
    if errors:
        return None, errors

    task = Task()
    task.title = data['title']
    task.description = data.get('description', '')
    task.status = data.get('status', 'pending')
    task.priority = data.get('priority', 3)
    task.user_id = data.get('user_id')
    task.category_id = data.get('category_id')

    if data.get('due_date'):
        try:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return None, ['Formato de data inválido. Use YYYY-MM-DD']

    if data.get('tags'):
        tags = data['tags']
        task.tags = ','.join(tags) if isinstance(tags, list) else tags

    db.session.add(task)
    db.session.commit()
    return task, None


def update_task(task_id, data):
    task = Task.query.get(task_id)
    if not task:
        return None, ['Task não encontrada']

    if 'title' in data:
        if len(data['title']) < 3 or len(data['title']) > 200:
            return None, ['Título deve ter entre 3 e 200 caracteres']
        task.title = data['title']

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        if data['status'] not in ['pending', 'in_progress', 'done', 'cancelled']:
            return None, ['Status inválido']
        task.status = data['status']

    if 'priority' in data:
        if not isinstance(data['priority'], int) or data['priority'] < 1 or data['priority'] > 5:
            return None, ['Prioridade deve ser entre 1 e 5']
        task.priority = data['priority']

    if 'user_id' in data:
        if data['user_id']:
            user = User.query.get(data['user_id'])
            if not user:
                return None, ['Usuário não encontrado']
        task.user_id = data['user_id']

    if 'category_id' in data:
        if data['category_id']:
            cat = Category.query.get(data['category_id'])
            if not cat:
                return None, ['Categoria não encontrada']
        task.category_id = data['category_id']

    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return None, ['Formato de data inválido']
        else:
            task.due_date = None

    if 'tags' in data:
        tags = data['tags']
        task.tags = ','.join(tags) if isinstance(tags, list) else tags

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return task, None


def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return False, 'Task não encontrada'
    db.session.delete(task)
    db.session.commit()
    return True, None


def search_tasks(query=None, status=None, priority=None, user_id=None):
    q = Task.query
    if query:
        q = q.filter(db.or_(Task.title.like(f'%{query}%'), Task.description.like(f'%{query}%')))
    if status:
        q = q.filter(Task.status == status)
    if priority:
        q = q.filter(Task.priority == int(priority))
    if user_id:
        q = q.filter(Task.user_id == int(user_id))
    return q.all()


def get_task_stats():
    from sqlalchemy import func
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    all_tasks = Task.query.all()
    overdue_count = sum(1 for t in all_tasks if t.is_overdue())

    return {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'cancelled': cancelled,
        'overdue': overdue_count,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
    }


def validate_task_data(data):
    errors = []
    if not data:
        return ['Dados inválidos']
    title = data.get('title')
    if not title:
        errors.append('Título é obrigatório')
    elif len(title) < 3 or len(title) > 200:
        errors.append('Título deve ter entre 3 e 200 caracteres')

    priority = data.get('priority', 3)
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        errors.append('Prioridade deve ser entre 1 e 5')

    status = data.get('status', 'pending')
    if status not in ['pending', 'in_progress', 'done', 'cancelled']:
        errors.append('Status inválido')

    if data.get('user_id'):
        user = User.query.get(data['user_id'])
        if not user:
            errors.append('Usuário não encontrado')

    if data.get('category_id'):
        cat = Category.query.get(data['category_id'])
        if not cat:
            errors.append('Categoria não encontrada')

    return errors
