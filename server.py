from flask import Flask, render_template, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def home():
    return render_template('index.html', title='Pictochat', heading='Select a Name')

@app.route('/room')
def room():
    return render_template('room.html', title='Pictochat', heading='Room A')
    

@sock.route('/chatroom')
def reverse(ws):
    while True:
        msg = ws.receive()
        data = json.loads(msg)
        if msg:
            print(f"Message recieved!\n From: {data['name']} \n Content: {data['msg']} \n Time: {data['time']}")
        ws.send(msg)

if __name__ == "__main__" :
    app.run(debug = True, host = "0.0.0.0")