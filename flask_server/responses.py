from flask import Blueprint, jsonify

responses_blueprint = Blueprint('', __name__)

@responses_blueprint.app_errorhandler(401)
def unauthorized(error):
    response = jsonify(
            {
                "return_code": 401,
                "message": "Unauthorized"
            })
    response.status_code = 401
    return response

