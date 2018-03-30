from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('move')
def test_message(message):
    emit('answer', {'data': message})

socketio.run(app, host='0.0.0.0')