from flask import Flask, jsonify, g

from flask_cors	import CORS 
from resources.coffees import coffee

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)