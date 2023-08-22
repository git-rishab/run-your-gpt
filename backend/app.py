from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chatStream import chat, audio, audio_to_text
from routes.user import login, register

app = Flask(__name__)
CORS(app)

@app.route('/')
def welcome():
    return jsonify({'message':'Welcome to parent-guide', 'ok':True})

app.route('/chat', methods=['POST'])(chat)
app.route('/audio', methods=['POST'])(audio)
app.route('/audiototext', methods=['POST'])(audio_to_text)
app.route('/user/register', methods=['POST'])(register)
app.route('/user/login', methods=['POST'])(login)

if __name__ == '__main__':
    app.run()