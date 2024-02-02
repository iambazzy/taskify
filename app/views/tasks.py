from flask import Blueprint, request
from app.middleware.middleware import login_required
from app.schemas.schemas import TaskSchema
from marshmallow import ValidationError
from app.helpers.helpers import build_response
from app.repository.tasks import Task, TaskRepository
tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('/create', methods=['POST'])
@login_required
def create_task(decoded_token):
    user_id = decoded_token["user"]["user_id"]
    schema = TaskSchema()
    task_repo = TaskRepository()
    try:
        data = schema.load(request.get_json())
        task_to_create = Task(
            title=data["title"],
            body=data["body"],
            due_date=data["due_date"],
            completed=data["completed"]
        )
        created_task_id = task_repo.create_task(task_to_create, user_id)
        data['id'] = created_task_id
        return build_response(data, 'Task created successfully', True), 201
    except ValidationError as error:
        return build_response(error.messages, 'An error occurred', False), 500

# @tasks_bp.route('/', methods=['GET'])
# @login_required
# def get_tasks(decoded_token):
#     try:
#         with db_connection_pool.getconn() as conn, conn.cursor() as cursor:
#             user_id = decoded_token["sub"]["user_id"]
#             fetch_tasks_query = 'SELECT * FROM user_tasks WHERE user_id = %s'
#             cursor.execute(fetch_tasks_query, (user_id,))
#             tasks = cursor.fetchall()
#             print(tasks, user_id)
#             tasks = [
#                 {
#                     'id': task[0],
#                     'title': task[2],
#                     'body': task[3],
#                     'due_date': task[4],
#                     'completed': task[5],
#                     "user_id": user_id
#                 } for task in tasks
#             ]
#             return build_response(tasks, 'Tasks fetched successfully', False), 200
#     except ValidationError as err:
#         return build_response(err.messages, 'An error occurred', False), 400
#     except Exception as e:
#         if 'conn' in locals():
#             conn.rollback()
#         current_app.logger.info(f"Error occurred during registration: {e}")
#         return build_response(e, 'An error occurred', False), 500
#     finally:
#         if 'conn' in locals():
#             db_connection_pool.putconn(conn)


# @tasks_bp.route('/update', methods=['PUT'])
# @login_required
# def update_task(decoded_token):
#     try:
#         with db_connection_pool.getconn() as conn, conn.cursor() as cursor:
#             user_id = decoded_token["sub"]["user_id"]
#                 update_task_query = 'UPDATE '
#     except ValidationError as err:
#         return build_response(err.messages, 'An error occurred', False), 400
#     except Exception as e:
#         if 'conn' in locals():
#             conn.rollback()
#         current_app.logger.info(f"Error occurred during registration: {e}")
#         return build_response(e, 'An error occurred', False), 500
#     finally:
#         if 'conn' in locals():
#             db_connection_pool.putconn(conn)
