import datetime
from peewee import *

DATABASE = SqlDatabase('coffees.sqlite')

class Coffee(Model):
	name = CharField()
	origin = CharField()
	acidity = CharField()
	created_at = DateTimeField(default=datetime.datetime.now) 