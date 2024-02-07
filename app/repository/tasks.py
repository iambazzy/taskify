from db.database import db_cursor
from flask import current_app


class Task:
    def __init__(self, title, body, due_date, completed):
        self.title = title
        self.body = body
        self.due_date = due_date
        self.completed = completed


class TaskRepository:
    @staticmethod
    def create_task(task, user_id):
        task_insert_query = f'''
            INSERT INTO user_tasks (user_id, title, body, due_date, completed)
            VALUES ({user_id}, '{task.title}', '{task.body}', '{task.due_date}', {task.completed})
            RETURNING id
        '''
        try:
            with db_cursor(True) as cursor:
                cursor.execute(task_insert_query)
                task_id = cursor.fetchone()[0]
            return task_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during task creation: {e}")

    @staticmethod
    def get_user_tasks(user_id):
        task_fetch_query = f'''
            SELECT * FROM user_tasks where user_id = {user_id}
        '''
        try:
            with db_cursor() as cursor:
                cursor.execute(task_fetch_query)
                tasks = cursor.fetchall()
                tasks = [
                     {
                         'id': task[0],
                         'title': task[2],
                         'body': task[3],
                         'due_date': task[4],
                         'completed': task[5],
                         "user_id": user_id
                     } for task in tasks
                ]
                return tasks
        except Exception as e:
            current_app.logger.info(f"Error occurred during task creation: {e}")
