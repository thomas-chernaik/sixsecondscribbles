from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import make_response
from flask import send_file
from io import BytesIO
import base64

from flask_socketio import SocketIO, emit, join_room

from GameManager import Game
from BadlyPreservedPickles import BadlyPreservedPickles
app = Flask(__name__)
app.config['GAMES'] = {}
#turn debug on
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['pickler'] = BadlyPreservedPickles()
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
        app.config['GAMES'][code] = Game(code, request.form['guessTime'], socketio)
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

@app.route('/uploadImage', methods=['POST'])
def upload_image():
    file = request.json['image']
    to_pickle = (file, request.headers["card-name"])
    filename = app.config['pickler'].pickle(to_pickle, request.cookies["player"], 600)
    return filename

@app.route('/getImage/<filename>')
def get_image(filename):
    # Unpickle the object
    unpickled = app.config['pickler'].unpickle(filename + ".pickle")

    # Extract the base64-encoded image data from the data URL
    image_data_url = unpickled[0]
    _, encoded_image_data = image_data_url.split(',', 1)

    # Decode the base64-encoded image data
    try:
        image_data = base64.b64decode(encoded_image_data)
    except (TypeError, binascii.Error):
        return "Invalid image data"

    # Serve the image using Flask's send_file function
    try:
        image_buffer = BytesIO(image_data)
        return send_file(
            image_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=unpickled[1] + ".png"
        )
    except Exception as e:
        return str(e)

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

@socketio.on('vote_to_start')
def handle_vote(data):
    print('vote_to_start')
    room = data['room']
    player = data['player']
    app.config['GAMES'][room].vote_to_start(player)

if __name__ == '__main__':
    socketio.run(app)