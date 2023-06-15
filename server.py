from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import autos


if __name__=='__main__':
    app.run(debug=True)

# from flask_app import app
# from flask_app.controllers import users, autos
# from flask import Flask, render_template, request, session
# from flask_socketio import SocketIO, join_room, emit, leave_room


# socketio = SocketIO(app)

# # Keep track of messages
# messages = {}

# @app.route('/chat/<int:id>', methods=['GET', 'POST'])
# def chat(id):
#     if request.method == 'POST':
#         recipient_id = request.form.get('recipient_id')
#         return render_template('chat.html', recipient_id=recipient_id, messages=messages.get(recipient_id, []))
#     else:
#         return render_template('chat.html', recipient_id=id, messages=messages.get(id, []))

# @socketio.on('connect')
# def handle_connect():
#     session['user_id'] = request.sid

# @socketio.on('join')
# def handle_join(data):
#     user_id = session.get('user_id')
#     room = data['room']
#     join_room(room)
#     emit('join_room', {'user_id': user_id}, room=room)

# @socketio.on('message')
# def handle_message(data):
#     sender_id = session.get('user_id')
#     recipient_id = data['recipient_id']
#     message = data['message']
#     room = recipient_id
#     if room not in messages:
#         messages[room] = []
#     messages[room].append({'sender_id': sender_id, 'message': message})
#     emit('message', {'sender_id': sender_id, 'message': message}, room=room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     leave_room(room)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
