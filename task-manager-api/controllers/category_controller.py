from database import db
from models.category import Category
from models.task import Task


def get_all_categories():
    categories = Category.query.all()
    result = []
    for c in categories:
        cat_data = c.to_dict()
        cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
        result.append(cat_data)
    return result


def get_category_by_id(cat_id):
    return Category.query.get(cat_id)


def create_category(data):
    if not data or not data.get('name'):
        return None, ['Nome é obrigatório']

    category = Category()
    category.name = data['name']
    category.description = data.get('description', '')
    category.color = data.get('color', '#000000')

    db.session.add(category)
    db.session.commit()
    return category, None


def update_category(cat_id, data):
    cat = Category.query.get(cat_id)
    if not cat:
        return None, ['Categoria não encontrada']

    if 'name' in data:
        cat.name = data['name']
    if 'description' in data:
        cat.description = data['description']
    if 'color' in data:
        cat.color = data['color']

    db.session.commit()
    return cat, None


def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return False, 'Categoria não encontrada'
    db.session.delete(cat)
    db.session.commit()
    return True, None
