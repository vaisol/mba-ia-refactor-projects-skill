import logging

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.notifications = []

    def notify_task_assigned(self, user, task):
        logger.info(f"Task '{task.title}' atribuída a {user.name}")
        self.notifications.append({
            'type': 'task_assigned',
            'user_id': user.id,
            'task_id': task.id
        })

    def notify_task_overdue(self, user, task):
        logger.info(f"Task '{task.title}' está atrasada! Usuário: {user.name}")

    def get_notifications(self, user_id):
        return [n for n in self.notifications if n['user_id'] == user_id]
