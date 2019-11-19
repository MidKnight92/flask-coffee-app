import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


user = Blueprint('users', 'user')

@user.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['email'].lower()
	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify(data={}, status={'code': 401, 'message': 'A user with that name already exists'})
	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		user = models.User.create(**payload)
		login_user(user)
		user_dict = model_to_dict(user)
		del user_dict['password']
		return jsonify(data=user_dict, status={'code': 201, 'message': 'Success'})

@user.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	#print(payload)
	try:
	 	user=models.User.get(models.User.email == payload['email'])
	 	user_dict = model_to_dict(user)
	 	if (check_password_hash(user_dict['password'], payload['password'])):
	 		del user_dict['password']
	 		login_user(user)
	 		return jsonify(data=user_dict, status={'code': 200, 'message': 'Success'}),200
	 	else:
	 		return jsonify(data={}, status={'code': 401, 'message': 'Username or  Password is incorrect'}),401
	except models.DoesNotExist:
	 	return jsonify(data={}, status={'code': 401, 'message': 'Username or Password is incorrect'}),401

@user.route('/', methods=['GET'])
def list_users():
	users = models.User.select()
	for u in users:
		user_dicts = [model_to_dict(u) for u in users]
	
	def remove_password(u):
		u.pop('password')
		return u

	user_dicts_without_pw = list(map(remove_password, user_dicts))

	return jsonify(data=user_dicts_without_pw), 200

@user.route('/logged_in', methods=['GET'])
def get_logged_in_user():
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'No user is currently logged in.'}),401
	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')
		return jsonify(data=user_dict, status={
			'code': 200,
			'message': 'Current user is {}'.format(user_dict['email'])
			}),200	


@user.route('/logout', methods=['GET'])
def logout():
	email = model_to_dict(current_user)['email']
	logout_user()

	return jsonify(data={}, status={
		'code': 200,
		'message': 'Logout Successful {}'.format(email)
		})














