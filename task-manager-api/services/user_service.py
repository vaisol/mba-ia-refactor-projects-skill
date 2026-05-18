from database import db
from models.user import User
from models.task import Task
import re
from sqlalchemy.orm import joinedload

class UserService:
    @staticmethod
    def get_all_users():
        # Solves N+1 query by eagerly loading tasks
        return User.query.options(joinedload(User.tasks)).all()

    @staticmethod
    def get_user_by_id(user_id):
        # Solves N+1 by eager load
        return User.query.options(joinedload(User.tasks)).get(user_id)

    @staticmethod
    def create_user(data):
        if not data:
            raise ValueError('Dados inválidos')

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            raise ValueError('Nome é obrigatório')
        if not email:
            raise ValueError('Email é obrigatório')
        if not password:
            raise ValueError('Senha é obrigatória')

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise ValueError('Email inválido')

        if len(password) < 4:
            raise ValueError('Senha deve ter no mínimo 4 caracteres')

        existing = User.query.filter_by(email=email).first()
        if existing:
            raise ValueError('Email já cadastrado')

        if role not in ['user', 'admin', 'manager']:
            raise ValueError('Role inválido')

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None

        if not data:
            raise ValueError('Dados inválidos')

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                raise ValueError('Email inválido')

            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise ValueError('Email já cadastrado')
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < 4:
                raise ValueError('Senha muito curta')
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                raise ValueError('Role inválido')
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False

        # Cascade delete is better, but we do it manually if not configured
        tasks = Task.query.filter_by(user_id=user_id).all()
        for t in tasks:
            db.session.delete(t)

        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def login(email, password):
        if not email or not password:
            raise ValueError('Email e senha são obrigatórios')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise ValueError('Credenciais inválidas')

        if not user.active:
            raise ValueError('Usuário inativo')

        return user
