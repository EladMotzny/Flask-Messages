from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from models import Message, db
import os.path



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db.init_app(app)

#initialize the db if it doesnt exist
if not os.path.isfile('messages.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html') 


#WRITE MESSAGE TO A SPECIFIC PERSON(POST)
#NEED TRY/EXCEPT
@app.route('/send/<string:reciever>', methods=['POST'])
def send_message(reciever):
    data = request.get_json()
    new_message = Message(sender = data['sender'], 
                            reciever=reciever, 
                            message = data['message'],
                            subject = data['subject'])
    db.session.add(new_message)
    db.session.flush()
    db.session.commit()
    return "Message: "+data['message']+" was sent to: " +reciever+ " and has the id: " + str(new_message.id)


#GET ALL MESSAGES FOR SPECIFIC USER (GET)
@app.route('/messages/<string:user>', methods=['GET'])
def get_messages(user):
    pass

#GET ALL UNREAD MESSAGES FOR A SPECIFIC USER (ANOTHER MODEL? OR TO ADD ANOTHER VARIABLE (BOOLEAN) TO CURRENT MODEL OF READ MESSAGE AND FILTER BY RECIEVER AND READ )
@app.route('/unread/<string:user>', methods=['GET'])
def get_unread_messages(user):
    pass

#READ MESSAGE (GET)
#WORKING
#ADD TRY/EXCEPT?
@app.route('/read/<int:id>', methods=['GET'])
def read_message(id):
    message = Message.query.get_or_404(id)
    message.read = True
    db.session.commit()
    return "Message: " + message.message + " was marked as read: " + str(message.read)


#DELETE MESSAGE (DEL)
#WORKING
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return "Message was deleted"



if __name__ == "__main__":
    app.run(debug=True)
