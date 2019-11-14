import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

coffee = Blueprint('coffees', 'coffee')

@dog.route('/', methods=["GET"])
def get_all_coffees():
	try:
		coffees = [model_to_dict(coffee) for coffee in models.Coffee.select()]
		print(coffees)
		return jsonify(data=coffees, status={"code":200, "message":"Success" })
		return jsonify(data={}, status={"code":401,"message": "Error getting the resources"})