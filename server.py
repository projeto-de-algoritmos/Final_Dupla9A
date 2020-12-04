from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from shortest_path import build_and_solve

socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('solve')
def handle_solve(graph_data):
    build_and_solve(graph_data['graph'], graph_data['start'], graph_data['goal'], socketio)


if __name__ == '__main__':
    socketio.run(app)
