from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html', title='Pictochat', heading='Select a Name')

@app.route('/room')
def room():
    return render_template('room.html', title='Pictochat', heading='Welcome to Pictochat!')

@socketio.on('message')
def handle_message(msg):
    data = json.loads(msg)
    print(f"Message From: {data['name']}: {data['msg']} \n Time: {data['time']}")
    emit('message', msg, broadcast=True)
    print(f"Message returned: {msg}")


if __name__ == "__main__" :
    socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)