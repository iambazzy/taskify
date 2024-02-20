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
            SELECT * FROM user_tasks WHERE user_id = {user_id}
        '''
        try:
            with db_cursor(True) as cursor:
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
            current_app.logger.info(f"Error occurred during user task fetching: {e}")

    @staticmethod
    def fetch_task(task_id):
        task_fetch_query = f'''
            SELECT * FROM user_tasks WHERE id = {task_id}
        '''
        try:
            with db_cursor() as cursor:
                cursor.execute(task_fetch_query)
                task = cursor.fetchone()
                return {
                 'id': task[0],
                 'title': task[2],
                 'body': task[3],
                 'due_date': task[4],
                 'completed': task[5],
                 "user_id": task[1]
                }
        except Exception as e:
            current_app.logger.info(f"Error occurred during task fetching: {e}")

    @staticmethod
    def update_task(task_id, data_to_update):
        task_update_query = f'''
            UPDATE user_tasks 
            SET title = '{data_to_update["title"]}', completed = {data_to_update["completed"]},
            due_date = '{data_to_update["due_date"]}', body = '{data_to_update["body"]}'
            WHERE id = {task_id} RETURNING id
        '''
        try:
            with db_cursor(True) as cursor:
                cursor.execute(task_update_query)
                updated_task_id = cursor.fetchone()[0]
                return updated_task_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during task updation: {e}")