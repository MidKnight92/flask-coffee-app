import datetime
from peewee import *

from flask_login import UserMixin

DATABASE = SqliteDatabase('coffees.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email=CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

class Coffee(Model):
	name = CharField()
	origin = CharField()
	acidity = CharField()
	created_at = DateTimeField(default=datetime.datetime.now) 

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Coffee], safe=True)
	print('TABLES CREATED!!')
	DATABASE.close()		

