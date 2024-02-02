from flask import request, jsonify
from app.helpers.helpers import build_response
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from functools import wraps


def login_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return build_response({}, 'Token is missing from the request', False), 401
        try:
            token_part = token.split(" ")[1]
            decoded_token = jwt.decode(token_part, 'your_secret_key', algorithms=["HS256"])
            kwargs['decoded_token'] = decoded_token
            return f(*args, **kwargs)
        except ExpiredSignatureError:
            return build_response({}, "Token has expired", False), 401
        except DecodeError:
            return build_response({}, "Token is invalid", False), 401
        except InvalidTokenError:
            return build_response({}, "Invalid token", False), 401
    return check_token
