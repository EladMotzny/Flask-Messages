from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Message, db
import os.path



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db.init_app(app)


#initialize the db if it doesnt exist
if not os.path.isfile('messages.db'):
    with app.app_context():
        db.create_all()


#Send a message to someone.
#Example: localhost:5000/send/Shlomi
@app.route('/send/<string:reciever>', methods=['POST'])
def send_message(reciever):
    try:
        data = request.get_json()
        new_message = Message(sender = data['sender'], 
                            reciever=reciever, 
                            message = data['message'],
                            subject = data['subject'])
        db.session.add(new_message)
        db.session.flush()
        db.session.commit()
        return "Message: "+data['message']+" was sent to: " +reciever+ " and has the id: " + str(new_message.id)
    except Exception as e:
        return jsonify({'Exception': True, 'Error:': str(e) + " Was not found"})

#Get all messages for user
#Example: localhost:5000/messages/Shlomi
@app.route('/messages/<string:user>', methods=['GET'])
def get_messages(user):
    try:
        all_messages = Message.query.filter_by(reciever = user).all()
        if all_messages is None:
            return "There are no messages for " + user
        return jsonify([e.serialize() for e in all_messages])
    except Exception as e:
        return jsonify({'Exception': True, 'Error:': str(e)})

#Get all unread messages for user
#Example: localhost:5000/unread/Shlomi
@app.route('/unread/<string:user>', methods=['GET'])
def get_unread_messages(user):
    try:
        all_messages = Message.query.filter_by(reciever = user, read = False).all()
        if all_messages is None:
            return "There are no messages for " + user
        return jsonify([e.serialize() for e in all_messages])
    except Exception as e:
        return jsonify({'Exception': True, 'Error:': str(e)})


#Read a specific message using the ID for that message
#Example: localhost:5000/read/1
@app.route('/read/<int:id>', methods=['GET'])
def read_message(id):
    try:
        message = Message.query.get_or_404(id)
        message.read = True
        db.session.commit()
        return "Message: " + message.message + " was marked as read"
    except Exception as e:
        return jsonify({'Exception': True, 'Error:': str(e)})


#Delete a message using the ID for that message
#Example: localhost:5000/delete/1
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_message(id):
    try:
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return "Message was deleted"
    except Exception as e:
        return jsonify({'Exception': True, 'Error:': str(e)})



if __name__ == "__main__":
    app.run(debug=True)
