from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send, emit
import json


envVars = []
try:
    with open('.env.local') as file:
        envVars = file.read()
except FileNotFoundError:
    print(".env.local file not found")

app = Flask(__name__)
app.config['SECRET_KEY'] = envVars[0]
socketio = SocketIO(app)
activeConnections = []

@app.route('/')
def home():
    return render_template('index.html', title='Pictochat', heading='Select a Name')

@app.route('/room')
def room():
    return render_template('room.html', title='Pictochat', heading='Welcome to Pictochat!')

@socketio.on('joinedRoom')
def handle_connect(joinedRoomMsg):
    data = json.loads(joinedRoomMsg)
    for user in activeConnections:
        if user[0] == data['name']:
            emit('nameExists', joinedRoomMsg, to=request.sid)
            print(f"Name {data['name']} already exists. Connection rejected.")
            return
    if(len(activeConnections) == 0):
        emit('hostAssigned', joinedRoomMsg, to=request.sid)
    activeConnections.append((data['name'], request.sid))
    print(f"{data['name']} has joined the room at {data['time']}")
    print(f"Active Connections: {activeConnections}")
    emit('joinedRoom', joinedRoomMsg, broadcast = True)

@socketio.on('leftRoom')
def handle_disconnect(leftRoomMsg):
    data = json.loads(leftRoomMsg)
    print(f"{data['name']} has left the room at {data['time']}")
    activeConnections.remove((next(user for user in activeConnections if user[0] == data['name'])))
    print(f"Active Connections: {activeConnections}")
    emit('leftRoom', leftRoomMsg, broadcast = True)

@socketio.on('message')
def handle_message(msg):
    data = json.loads(msg)
    print(f"Message From: {data['name']}: {data['payload']['msg']} \n Time: {data['time']}")
    emit('message', msg, broadcast=True)


if __name__ == "__main__" :
    socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)