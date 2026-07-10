from database import db
from models.user import User
from models.task import Task
import re


def get_all_users():
    users = User.query.all()
    result = []
    for u in users:
        data = u.to_dict()
        data['task_count'] = len(u.tasks)
        result.append(data)
    return result


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return [t.to_dict() for t in tasks]


def create_user(data):
    errors = validate_user_data(data)
    if errors:
        return None, errors

    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return None, ['Email já cadastrado']

    user = User()
    user.name = data['name']
    user.email = data['email']
    user.set_password(data['password'])
    user.role = data.get('role', 'user')

    db.session.add(user)
    db.session.commit()
    return user, None


def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None, ['Usuário não encontrado']

    if 'name' in data:
        user.name = data['name']

    if 'email' in data:
        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
            return None, ['Email inválido']
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return None, ['Email já cadastrado']
        user.email = data['email']

    if 'password' in data:
        if len(data['password']) < 4:
            return None, ['Senha deve ter no mínimo 4 caracteres']
        user.set_password(data['password'])

    if 'role' in data:
        if data['role'] not in ['user', 'admin', 'manager']:
            return None, ['Role inválido']
        user.role = data['role']

    if 'active' in data:
        user.active = data['active']

    db.session.commit()
    return user, None


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, 'Usuário não encontrado'
    tasks = Task.query.filter_by(user_id=user_id).all()
    for t in tasks:
        db.session.delete(t)
    db.session.delete(user)
    db.session.commit()
    return True, None


def login(email, password):
    if not email or not password:
        return None, 'Email e senha são obrigatórios'

    user = User.query.filter_by(email=email).first()
    if not user:
        return None, 'Credenciais inválidas'
    if not user.check_password(password):
        return None, 'Credenciais inválidas'
    if not user.active:
        return None, 'Usuário inativo'

    return {
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token': 'fake-jwt-token-' + str(user.id)
    }, None


def validate_user_data(data):
    errors = []
    if not data:
        return ['Dados inválidos']
    if not data.get('name'):
        errors.append('Nome é obrigatório')
    if not data.get('email'):
        errors.append('Email é obrigatório')
    if not data.get('password'):
        errors.append('Senha é obrigatória')
    if data.get('password') and len(data['password']) < 4:
        errors.append('Senha deve ter no mínimo 4 caracteres')
    if data.get('email') and not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
        errors.append('Email inválido')
    if data.get('role') and data['role'] not in ['user', 'admin', 'manager']:
        errors.append('Role inválido')
    return errors
