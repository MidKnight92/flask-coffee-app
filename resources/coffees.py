import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

coffee = Blueprint('coffees', 'coffee')

# Index Route
@coffee.route('/', methods=["GET"])
@login_required
def get_creators_coffees():
	try:
		this_users_coffee_instances = models.Coffee.select().where(models.Coffee.creator_id == current_user.id)
		coffees = [model_to_dict(coffee) for coffee in this_users_coffee_instances]
		print(coffees)
		return jsonify(data=coffees, status={"code":200, "message":"Success" }), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"}), 401

#Create Route
@coffee.route('/', methods=['POST'])
@login_required
def create_coffee():
	payload = request.get_json()
	# print(type(payload), 'payload')
	coffee = models.Coffee.create(name=payload['name'], origin=payload['origin'], acidity=['acidity'], creator=current_user.id)
	# print(coffee.__dict__)
	# print(dir(coffee))
	# print(model_to_dict(coffee), '<<<<<<<<This is model to dict')
	coffee_dict = model_to_dict(coffee)
	coffee_dict['creator'].pop('password')
	return jsonify(data=coffee_dict, status={'code': 201, 'message': 'Created - Success'}), 201

#This route allows creators to create their own coffee cards by taking in their id as props and then saving their id in the api when they create the coffee
@coffee.route('/<creator_id>', methods=['POST'])
def create_coffee_associated_with_creator(creator_id):
	payload = request.get_json()
	# print(type(payload), 'payload')
	coffee = models.Coffee.create(name=payload['name'], origin=payload['origin'], acidity=['acidity'], creator=creator_id)
	coffee_dict = model_to_dict(coffee)
	coffee_dict['creator'].pop('password')
	return jsonify(data=coffee_dict, status={'code': 201, 'message': 'Created - Success'}), 201


#Update Route
@coffee.route('/<id>', methods=['PUT'])
@login_required
def update_coffee(id):
	payload = request.get_json()
	coffee = models.Coffee.get_by_id(id)

	if(coffee.creator.id == current_user.id):
		coffee.name = payload['name'] if 'name' in payload else None
		coffee.origin = payload['origin'] if 'origin' in payload else None
		coffee.acidity = payload['acidity'] if 'acidity' in payload else None

		coffee.save()	

		coffee_dict = model_to_dict(coffee)
		coffee_dict['creator'].pop('password')

		return jsonify(data=coffee_dict, status={'code': 200, 'message': 'OK'}), 200
	else:
		return jsonify(data="Forbidden", status={ 'code': 403, 'message': 'Only the creator can update their coffee creation.'}), 403	

#Show Route
@coffee.route('/<id>', methods=['GET'])
def show_coffe(id):
	print(id)
	coffee = models.Coffee.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(data={'name': coffee.name, 'origin': coffee.origin}, status={'code': 200, 'message': 'Registered users can access more info.'}), 200
	else:	
		coffee_dict = model_to_dict(coffee)
		coffee_dict['coffee'].pop('password')

		if coffee.creator_id != current_user.id:
			coffee_dict.pop('created_at')

		return jsonify(data=coffee_dict, status={'code': 200, 'message': 'Coffee id: {}'.format(coffee.id)}), 200	

#Delete Route 
@coffee.route('/<id>', methods=['Delete'])
@login_required
def delete_coffee(id):
	coffee_to_delete = models.Coffee.get_by_id(id)

	if coffee_to_delete.creator.id != current_user.id:
		return jsonify(data='Forbidden', status={
			'code': 403,
			'message': 'Forbidden: Only the creator can do that.'
			}), 403
	else:	
		coffee_name = coffee_to_delete.name
		coffee_to_delete.delete_instance()
		return jsonify(data='DELETED', status={'code': 200, 'message': 'Deleted'})









