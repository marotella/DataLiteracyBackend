from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import models


placementCriteria = Blueprint("criteria", __name__)

#INDEX
@placementCriteria.route("/", methods=["GET"])
@login_required
def get_all_critera():
    payload=request.get_json()
    try:
        criteria = [model_to_dict(criteria) for criteria in current_user.placement_criteria]
        return jsonify(data=criteria, status={"code":200, "message": "Successfully retrieved criteria"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
    
## CREATE
@placementCriteria.route("/", methods=["POST"])
@login_required
def create_criteria():
    payload = request.get_json()
    try:
        criteria = models.PlacementCriteria.create(
        user=current_user.id,
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
    except Exception as e:
        return jsonify(data={}, status={"code":400, "message": str(e)})
    
        
## DELETE
@placementCriteria.route("/<int:criteria_id>", methods = ["DELETE"])
@login_required
def delete_criteria(criteria_id):
    try:
        criteria= models.PlacementCriteria.get((models.PlacementCriteria.id == criteria_id)&(models.PlacementCriteria.user == current_user))
        criteria.delete_instance()
        return jsonify(data={}, status={"code":201, "message":"Successfully deleted criteria"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message":"Criteria not found."})
    
    
## UPDATE
@placementCriteria.route("/<int:criteria_id>", methods=["PUT"])
@login_required
def update_criteria(criteria_id):
    payload = request.get_json()
    try:
        criteria = models.PlacementCriteria.get((models.PlacementCriteria.id == criteria_id)&(models.PlacementCriteria.user == current_user))
        criteria.update(**payload).execute()
        updated_criteria = model_to_dict(update_criteria)
        criteria_dict = model_to_dict(update_criteria)
        return jsonify(data=criteria_dict, status={"code": 200, "message":"Criteria updated."})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code":404, "message":"Criteria not found."})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})