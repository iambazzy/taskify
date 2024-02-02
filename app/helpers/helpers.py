from flask import jsonify


def build_response(data, message, success):
    final = {
        'message': message,
        'success': success,
        'data': data
    }
    return final
