from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import models


placementCriteria = Blueprint("criteria", __name__)

#INDEX - View all criteria created for a user
@placementCriteria.route("/", methods=["GET"])
@jwt_required() #check to make sure a user is logged in
def get_all_critera():
    payload=request.get_json()
    current_user_id = get_jwt_identity()  
    try:
        criteria = [model_to_dict(criteria) for criteria in current_user_id.placement_criteria] #query for the criteria linked to the current user
        return jsonify(data=criteria, status={"code":200, "message": "Successfully retrieved criteria"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
    
## CREATE allows the user to add new placement criteria for an intervention
@placementCriteria.route("/", methods=["POST"])
@jwt_required()
def create_criteria():
    payload = request.get_json()
    current_user_id = get_jwt_identity()

    try:
        criteria = models.PlacementCriteria.create(
        user=current_user_id,
        interventionName = payload["interventionName"],
        screenerScoreMax = payload["screenerScoreMax"],
        decodingScoreMax = payload["decodingScoreMax"],
        encodingScoreMax = payload["encodingScoreMax"],
        screenerScoreMin = payload["screenerScoreMin"],
        decodingScoreMin = payload["decodingScoreMin"],
        encodingScoreMin = payload["encodingScoreMin"]
        )
        criteria_dict = model_to_dict(criteria)
        return jsonify(data=criteria_dict, status={"code": 201, "message":"Successfully created intervention criteria."})
    except Exception as e: ## add in a check for the intervention already existing 
        return jsonify(data={}, status={"code":400, "message": str(e)})
    
        
## DELETE
@placementCriteria.route("/<int:criteria_id>", methods = ["DELETE"])
@jwt_required()
def delete_criteria(criteria_id):
    current_user_id = get_jwt_identity()

    try:
        criteria= models.PlacementCriteria.get((models.PlacementCriteria.id == criteria_id)&(models.PlacementCriteria.user == current_user_id)) #query for the criteria that alings to the current user
        criteria.delete_instance()
        return jsonify(data={}, status={"code":201, "message":"Successfully deleted criteria"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message":"Criteria not found."})
    
    
## UPDATE the placement criteria for the current  user
@placementCriteria.route("/<int:criteria_id>", methods=["PUT"])
@jwt_required()
def update_criteria(criteria_id):
    payload = request.get_json()
    current_user_id = get_jwt_identity()

    try:
        criteria = models.PlacementCriteria.get((models.PlacementCriteria.id == criteria_id)&(models.PlacementCriteria.user == current_user_id)) # query the criteria for the current user 
        criteria.update(**payload).execute() # execute the update 
        updated_criteria = model_to_dict(update_criteria)
        criteria_dict = model_to_dict(update_criteria)
        return jsonify(data=criteria_dict, status={"code": 200, "message":"Criteria updated."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code":404, "message":"Criteria not found."})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})