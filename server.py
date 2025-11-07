from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def home():
    return render_template('index.html', title='My Flask App', heading='Hello from Flask!')
    

@sock.route('/reverse')
def reverse(ws):
    while True:
        text = ws.receive()
        if text:
            print(f"Message recieved: {text}")
        ws.send(text[::-1])

if __name__ == "__main__" :
    app.run(debug = True, host = "0.0.0.0")