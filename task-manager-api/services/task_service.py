from models.task import Task
from database import db
from sqlalchemy.orm import joinedload
from datetime import datetime

class TaskService:
    @staticmethod
    def get_all_tasks():
        # Solve N+1 with joinedload
        return Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()

    @staticmethod
    def create_task(data):
        task = Task()
        task.title = data.get('title')
        task.description = data.get('description', '')
        task.status = data.get('status', 'pending')
        task.priority = data.get('priority', 3)
        task.user_id = data.get('user_id')
        task.category_id = data.get('category_id')
        
        if data.get('due_date'):
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_task_details(task_id):
        task = Task.query.get(task_id)
        if not task:
            return None
        
        data = task.to_dict()
        data['overdue'] = task.is_overdue()
        return data
