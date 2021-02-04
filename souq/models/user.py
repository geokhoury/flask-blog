from mongoengine import *
from mongoengine.fields import StringField
from datetime import datetime


class User(Document):
    # define class metadata
    meta = {'collection': 'users'}

    # define class fields
    username = StringField(required=True,unique=True)
    birthday = DateTimeField(required=True) 
    email= StringField(required=True,max_length=250)
    status = StringField(default='user')
    password = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    biography = StringField(max_length=250)
    created_at = DateTimeField(default=datetime.utcnow)

    def get_by_username(cls, username):
        data = User.objects.get(username= username)
        if data is not None:
            return data
    
    def change_password(self, current_password, new_password):
        if current_password == self.password:
            self.password = (new_password)
            return True
        else:
            return False

    def serialize(self):
        serialized = {
            "id": str(self.pk),
            'username': self.username,
            'password': 'nice try :)!',
            'status': self.status,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'biography': self.biography,
            'status':self.status,
                    }
        return serialized
    
