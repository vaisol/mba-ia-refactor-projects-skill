from database import db
from models.category import Category
from models.task import Task
from sqlalchemy import func

class CategoryService:
    @staticmethod
    def get_all_categories():
        # Eager load task count using group_by
        categories = Category.query.all()
        # Alternatively, we could do a join, but for simplicity:
        result = []
        for c in categories:
            cat_data = c.to_dict()
            cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
            result.append(cat_data)
        return result

    @staticmethod
    def create_category(data):
        if not data:
            raise ValueError('Dados inválidos')

        name = data.get('name')
        if not name:
            raise ValueError('Nome é obrigatório')

        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')

        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update_category(cat_id, data):
        cat = Category.query.get(cat_id)
        if not cat:
            return None

        if 'name' in data:
            cat.name = data['name']
        if 'description' in data:
            cat.description = data['description']
        if 'color' in data:
            cat.color = data['color']

        db.session.commit()
        return cat

    @staticmethod
    def delete_category(cat_id):
        cat = Category.query.get(cat_id)
        if not cat:
            return False

        db.session.delete(cat)
        db.session.commit()
        return True
