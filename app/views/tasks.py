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


@tasks_bp.route('/', methods=['GET'])
@login_required
def get_tasks(decoded_token):
    try:
        task_repo = TaskRepository()
        user_id = decoded_token["user"]["user_id"]
        tasks = task_repo.get_user_tasks(user_id)
        return build_response(tasks, 'Tasks fetched successfully', True), 200
    except Exception as e:
        return build_response(e, 'An error occurred', False), 500


@tasks_bp.route('/update_task/<task_id>', methods=['PUT'])
@login_required
def update_task(decoded_token, task_id):
    schema = TaskSchema()
    try:
        data = schema.load(request.get_json())
        task_repo = TaskRepository()
        user_id = decoded_token['user']['user_id']
        task_in_db = task_repo.fetch_task(task_id)
        if not task_in_db:
            return build_response({}, 'Task not found', False), 400
        if user_id != task_in_db['user_id']:
            return build_response({}, 'Not authorized to perform this operation', False), 401
        updated_task_id = task_repo.update_task(task_id, data)
        updated_task = task_repo.fetch_task(updated_task_id)
        return build_response(updated_task, 'Task updated successfully', True), 200
    except ValidationError as error:
        return build_response(error.messages, 'An error occurred', False), 500


@tasks_bp.route('/delete_task/<task_id>', methods=['DELETE'])
@login_required
def delete_task(decoded_token, task_id):
    try:
        task_repo = TaskRepository()
        user_id = decoded_token['user']['user_id']
        task_in_db = task_repo.fetch_task(task_id)
        if not task_in_db:
            return build_response({}, 'Task not found', False), 400
        if user_id != task_in_db['user_id']:
            return build_response({}, 'Not authorized to perform this operation', False), 401
        deleted_task_id = task_repo.delete_task(task_id)
        return build_response({'id': deleted_task_id}, 'Task deleted successfully', True), 200
    except Exception as e:
        return build_response(e, 'An error occurred', False), 500
