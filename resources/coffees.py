import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

coffee = Blueprint('coffees', 'coffee')

# Index Route
@coffee.route('/', methods=["GET"])
def get_all_coffees():
	try:
		coffees = [model_to_dict(coffee) for coffee in models.Coffee.select()]
		print(coffees)
		return jsonify(data=coffees, status={"code":200, "message":"Success" })
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#Create Route
@coffee.route('/', methods=['POST'])
def create_coffees():
	payload = request.get_json()
	print(type(payload), 'payload')
	coffee = models.Coffee.create(**payload)
	print(coffee.__dict__)
	print(dir(coffee))
	print(model_to_dict(coffee), '<<<<<<<<This is model to dict')
	coffee_dict = model_to_dict(coffee)
	return jsonify(data=coffee_dict, status={'code': 201, 'message': 'Created - Success'})