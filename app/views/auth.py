from flask import Blueprint, request
from app.schemas.schemas import RegisterSchema, LoginSchema, ResetPassword, UpdatePassword
from marshmallow import ValidationError
from app.helpers.helpers import build_response
from app.repository.auth import AuthRepository, User

auth_bp = Blueprint('auth_bp', __name__, url_prefix="/auth")


@auth_bp.route('/register', methods=['POST'])
def register_user():
    schema = RegisterSchema()
    auth_repo = AuthRepository()
    try:
        data = schema.load(request.get_json())
        user = auth_repo.user_exists(data["email"])
        if user:
            return build_response({}, 'User already exists', False), 409
        user_to_register = User(
            first_name=data["firstname"],
            last_name=data["lastname"],
            email=data["email"],
            password=auth_repo.hash_password(data["password"])
        )
        saved_user_id = auth_repo.save_user(user_to_register)
        return build_response({"user_id": saved_user_id}, 'User registered successfully', True), 201
    except ValidationError as err:
        return build_response(err.messages, 'An error occurred', False), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    auth_repo = AuthRepository()
    try:
        data = schema.load(request.get_json())
        user = auth_repo.user_exists(data["email"])
        if not user:
            return build_response({}, 'User does not exist', False), 400
        if not auth_repo.is_password_valid(user['password'], data['password']):
            return build_response({}, 'Email or password is wrong', False), 400
        jwt_token = auth_repo.create_token({"user_id": user["user_id"], "email": user["email"]})
        user['token'] = jwt_token['jwt_token']
        del user['password']
        return build_response(user, 'Logged in successfully ', True), 200
    except ValidationError as err:
        return build_response(err.messages, 'An error occurred', False), 500


@auth_bp.route('/reset-password', methods=["POST", "PUT"])
def reset_password():
    auth_repo = AuthRepository()
    try:
        # HANDLE POST REQUEST
        if request.method == 'POST':
            schema = ResetPassword()
            data = schema.load(request.get_json())
            user = auth_repo.user_exists(data["email"])

            if not user:
                return build_response({}, 'User does not exist', False), 400

            token_data = auth_repo.create_token({"user_id": user["user_id"], "email": user["email"]})
            reset_url = f'app.bazzy.com?token={token_data["jwt_token"]}'
            saved_token_id = auth_repo.save_token({
                "user_id": user['user_id'],
                "token": token_data["jwt_token"],
                "issued_at": token_data["payload"]["iat"],
                "expires_at": token_data["payload"]["exp"]
            })

            if saved_token_id:
                return build_response({"reset_url": reset_url}, 'Email sent successfully', True), 200

        # HANDLE UPDATE REQUEST
        if request.method == 'PUT':
            schema = UpdatePassword()
            data = schema.load(request.get_json())
            token_in_db = auth_repo.token_exists(data['token'])

            if not token_in_db:
                return build_response({}, 'Token does not exist', False), 404
            decoded_token = auth_repo.validate_token(data['token'], 'your_secret_key')

            if not decoded_token["valid"]:
                return build_response(decoded_token, 'Token is invalid', False), 401

            user_id = decoded_token['payload']['user']['user_id']
            new_hashed_password = auth_repo.hash_password(data['password'])
            updated_user_id = auth_repo.update_user_password(user_id, new_hashed_password)

            if not updated_user_id:
                return build_response({}, 'Something went wrong', False), 400

            auth_repo.remove_token(token_in_db['id'])
            return build_response({}, 'Password changed successfully', False), 200
    except ValidationError as err:
        return build_response(err.messages, 'An error occurred', False), 500
