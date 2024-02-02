from db.database import db_cursor
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from datetime import datetime, timedelta


class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class AuthRepository:
    @staticmethod
    def save_user(user):
        user_create_query = f'''
            INSERT INTO users (firstname, lastname, email, password)
            VALUES ('{user['first_name']}', '{user['last_name']}', '{user['email']}', '{user['password']}')
            RETURNING user_id
        '''
        try:
            with db_cursor(True) as cursor:
                print(cursor)
                cursor.execute(user_create_query)
                user_id = cursor.fetchone()[0]
            return user_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during user registration: {e}")

    @staticmethod
    def user_exists(email):
        user_exists_query = f'''
            SELECT * FROM users WHERE email = '{email}'
        '''
        try:
            with db_cursor(True) as cursor:
                cursor.execute(user_exists_query)
                user = cursor.fetchone()
                if user:
                    col_names = [desc[0] for desc in cursor.description]
                    user = dict(zip(col_names, user))
                    return user
                else:
                    return False
        except Exception as e:
            current_app.logger.info(f"Error occurred during user fetching: {e}")

    @staticmethod
    def save_token(data):
        token_save_query = f'''
           INSERT INTO password_reset_tokens (user_id, token, created_at, expires_at)
           VALUES ({data['user_id']}, '{data['token']}', '{data['issued_at']}', '{data['expires_at']}')
           RETURNING id
        '''
        try:
            with db_cursor(True) as cursor:
                cursor.execute(token_save_query)
                token_id = cursor.fetchone()[0]
                return token_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during token saving: {e}")

    @staticmethod
    def token_exists(token):
        # Fetch using token id later on
        token_get_query = f"SELECT * FROM password_reset_tokens WHERE token = '{token}'"
        try:
            with db_cursor(True) as cursor:
                cursor.execute(token_get_query)
                token = cursor.fetchone()
                if token:
                    col_names = [desc[0] for desc in cursor.description]
                    token = dict(zip(col_names, token))
                    return token
                else:
                    return False
        except Exception as e:
            current_app.logger.info(f"Error occurred during token saving: {e}")

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def is_password_valid(hashed_password, user_password):
        return check_password_hash(hashed_password, user_password)

    @staticmethod
    def validate_token(token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return {"valid": True, "payload": payload}
        except ExpiredSignatureError:
            return {"valid": False, "error": "Token has expired"}
        except DecodeError:
            return {"valid": False, "error": "Token is invalid"}
        except InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}

    @staticmethod
    def create_token(data_to_encode):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'user': data_to_encode
        }
        jwt_token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
        return {"jwt_token": jwt_token, "payload": payload}

    @staticmethod
    def update_user_password(user_id, password):
        update_password_query = f"UPDATE users SET password = '{password}' WHERE user_id = {user_id} RETURNING user_id"
        try:
            with db_cursor(True) as cursor:
                cursor.execute(update_password_query)
                user_id = cursor.fetchone()[0]
                return user_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during update password: {e}")

    @staticmethod
    def remove_token(token_id):
        delete_token_query = f'DELETE FROM password_reset_tokens WHERE id = {token_id} RETURNING id'
        try:
            with db_cursor(True) as cursor:
                cursor.execute(delete_token_query)
                token_id = cursor.fetchone()[0]
                return token_id
        except Exception as e:
            current_app.logger.info(f"Error occurred during removing token: {e}")