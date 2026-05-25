from .. import socketio
from flask_socketio import emit, join_room

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def on_join(data):
    room = data['user_id']
    join_room(room)
    print(f'User {room} joined their notification room')

@socketio.on('new_message')
def handle_message(data):
    recipient_id = data['recipient_id']
    emit('message_received', data, room=recipient_id)

def notify_hiring_status(user_id, status):
    socketio.emit('status_update', {'status': status}, room=str(user_id))
