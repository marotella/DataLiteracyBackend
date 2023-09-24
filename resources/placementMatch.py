from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from peewee import fn
from models import Student, PlacementCriteria, PlacementMatch

match = Blueprint('placement', __name__)

#MATCH
@match.route("/", methods=["POST"])
@jwt_required()
def match_student():
    current_user_id = get_jwt_identity()
    try:
        #pull student data from request
        data = request.get_json()
        student_id = data.get("student_id")
        
        #get it from the database
        student= Student.get(
            (student_id == student_id) & (Student.user == current_user_id)
        )
        #get all placement criteria
        criteria_list = PlacementCriteria.select()
        
        #Start matching
        #create variables needed
        best_fit_match = None
        min_score_difference = float("inf")
        
        for criteria in criteria_list:
            screener_diff = abs(student.screenerScore - criteria.screenerScoreMin)
            decoding_diff = abs(student.decodingScore - criteria.screenerScoreMin)
            encoding_diff = abs(student.encodingScore - criteria.encodingScoreMin)
            
            total_diff = screener_diff + decoding_diff + encoding_diff
            
            if total_diff < min_score_difference:
                min_score_difference = total_diff
                best_fit_match= criteria.interventionName
                
        intervention_match = PlacementMatch.create(
            student = student,
            intervention = best_fit_match,
            score_difference = min_score_difference
        )
                
        return jsonify({
            "best_fit_match": best_fit_match,
            "min_score_difference": min_score_difference,
            "match_id": intervention_match.id
        })
        
    except Student.DoesNotExist:
        return jsonify({"error": "Student not found"}, 404)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)