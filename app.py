from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_socketio import SocketIO, emit, join_room

from GameManager import Game
app = Flask(__name__)
app.config['GAMES'] = {}
#turn debug on
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

@app.route('/')
def main_page():  # put application's code here
    return render_template('home.html')

@app.route('/card')
def card():
    return render_template('card.html')

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/createGame', methods=['GET', 'POST'])
def create_game():
    #if post
    if request.method == 'POST':
        code = Game.generateCode()
        while code in app.config['GAMES']:
            code = Game.generateCode()
        app.config['GAMES'][code] = Game(code, request.form['guessTime'])
        app.config['GAMES'][code].add_player(request.form['player'])
        return code
    #if get
    return render_template('createGame.html')

@app.route('/waitingRoom/<code>')
def waiting_room(code):
    return render_template('waitingRoom.html', code=code)

@app.route('/joinGame', methods=['GET', 'POST'])
def join_game():
    #if post
    if request.method == 'POST':
        code = request.form['code']
        if code not in app.config['GAMES']:
            return redirect(url_for('bad_code'))

        app.config['GAMES'][code].add_player(request.form['player'])
        return code
    #if get
    return render_template('joinGame.html')

@app.route('/badCode')
def bad_code():
    return render_template('badCode.html')
@socketio.on('join')
def handle_join(data):
    room = data['room']
    print(room)
    join_room(room)
    print('Client joined room:', room)
    emit('player_joined', {'player': app.config['GAMES'][data['room']].getPlayers()}, room=data['room'])
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
if __name__ == '__main__':
    socketio.run(app)