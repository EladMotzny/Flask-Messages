from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    reciever  = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, nullable=False)

    #To print out when we send a new message for testing
    def __repr__(self):
        return "Message: " + str(self.message)

    #Serializer function to return to the user
    def serialize(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'reciever': self.reciever,
            'message': self.message,
            'subject': self.subject,
            'creation_date': self.creation_date,
            'read': self.read
        }

