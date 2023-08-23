from flask import request, jsonify
from config.db import user
from bson import ObjectId
from flask_jwt_extended import create_access_token
from models.User import User

# Route for registration of the user
def register():
    user_data = request.json
    user = User(user_data)
    response, status = user.save()
    return jsonify(response), status

# Route for authentiating the user
def login():
    login_data = request.json
    response = User.login(login_data['email'], login_data['password'])
    return jsonify(response)