from flask import Flask, jsonify, g
from flask_cors	import CORS 
from resources.coffees import coffee
from resources.user import user
from flask_login import LoginManager
import models

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = "This is my secret_key"

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None


@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

CORS(coffee, origins=['http://localhost:3000'], supports_credentials=True)	
app.register_blueprint(coffee, url_prefix='/api/v1/coffees')


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user, url_prefix='/api/v1/users')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)