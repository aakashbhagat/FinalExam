from database.db import db
from flask_bcrypt import check_password_hash, generate_password_hash

#Data Model for Books
class Books(db.Document):
    book_id = db.IntField(required=True, unique=True)
    author = db.StringField(required=True)    
    country = db.StringField(required=True)
    imageLink = db.StringField(required=True)
    language = db.StringField(required=True)
    link = db.StringField(required=True)
    pages = db.IntField(required=True)
    title = db.StringField(required=True)
    year = db.IntField(required=True)

class User(db.Document):
    
	email= db.EmailField(required=True,unique=True)
	password = db.StringField(required=True,min_length=6)

	def hash_password(self):
		self.password=generate_password_hash(self.password).decode('utf8')
	def check_password(self,password):
		 return check_password_hash(self.password,password)
