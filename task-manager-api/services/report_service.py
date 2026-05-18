from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime, timedelta
from sqlalchemy import func

class ReportService:
    @staticmethod
    def get_summary_report():
        total_tasks = db.session.query(Task).count()
        total_users = db.session.query(User).count()
        total_categories = db.session.query(Category).count()

        # Query by status
        status_counts = db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
        status_dict = {status: count for status, count in status_counts}
        
        pending = status_dict.get('pending', 0)
        in_progress = status_dict.get('in_progress', 0)
        done = status_dict.get('done', 0)
        cancelled = status_dict.get('cancelled', 0)

        # Query by priority
        priority_counts = db.session.query(Task.priority, func.count(Task.id)).group_by(Task.priority).all()
        priority_dict = {p: count for p, count in priority_counts}

        # Overdue tasks
        now = datetime.utcnow()
        overdue_tasks_query = db.session.query(Task).filter(
            Task.due_date < now,
            Task.status.notin_(['done', 'cancelled'])
        ).all()
        
        overdue_count = len(overdue_tasks_query)
        overdue_list = [{
            'id': t.id,
            'title': t.title,
            'due_date': str(t.due_date),
            'days_overdue': (now - t.due_date).days
        } for t in overdue_tasks_query]

        seven_days_ago = now - timedelta(days=7)
        recent_tasks = db.session.query(Task).filter(Task.created_at >= seven_days_ago).count()
        recent_done = db.session.query(Task).filter(
            Task.status == 'done',
            Task.updated_at >= seven_days_ago
        ).count()

        # User productivity solving N+1
        user_stats_query = db.session.query(
            User.id,
            User.name,
            func.count(Task.id).label('total_tasks'),
            func.sum(db.case((Task.status == 'done', 1), else_=0)).label('completed_tasks')
        ).outerjoin(Task, User.id == Task.user_id).group_by(User.id).all()

        user_stats = []
        for row in user_stats_query:
            total = row.total_tasks
            completed = row.completed_tasks or 0
            user_stats.append({
                'user_id': row.id,
                'user_name': row.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
            })

        return {
            'generated_at': str(now),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': {
                'critical': priority_dict.get(1, 0),
                'high': priority_dict.get(2, 0),
                'medium': priority_dict.get(3, 0),
                'low': priority_dict.get(4, 0),
                'minimal': priority_dict.get(5, 0),
            },
            'overdue': {
                'count': overdue_count,
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }

    @staticmethod
    def get_user_report(user_id):
        user = db.session.query(User).get(user_id)
        if not user:
            return None

        tasks = db.session.query(Task).filter_by(user_id=user_id).all()

        total = len(tasks)
        done = 0
        pending = 0
        in_progress = 0
        cancelled = 0
        overdue = 0
        high_priority = 0

        now = datetime.utcnow()

        for t in tasks:
            if t.status == 'done':
                done += 1
            elif t.status == 'pending':
                pending += 1
            elif t.status == 'in_progress':
                in_progress += 1
            elif t.status == 'cancelled':
                cancelled += 1

            if t.priority <= 2:
                high_priority += 1

            if t.due_date and t.due_date < now and t.status not in ['done', 'cancelled']:
                overdue += 1

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
            }
        }
