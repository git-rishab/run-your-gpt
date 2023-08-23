from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chatStream import chat, audio, audio_to_text
from routes.user import login, register
from flask_jwt_extended import JWTManager, jwt_required
import os

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)


@app.route("/")
def welcome():
    return jsonify({"message": "Welcome to parent-guide", "ok": True})


@app.route("/chat", methods=["POST"])
@jwt_required()
def secure_chat_route():
    return chat()


@app.route("/audio", methods=["POST"])
@jwt_required()
def non_secure_audio_route():
    return audio()


@app.route("/audiototext", methods=["POST"])
def non_secure_audio_to_text_route():
    return audio_to_text()


@app.route("/user/register", methods=["POST"])
def non_secure_register_route():
    return register()


@app.route("/user/login", methods=["POST"])
def non_secure_login_route():
    return login()


if __name__ == "__main__":
    app.run()
