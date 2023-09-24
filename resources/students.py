from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import models

students = Blueprint('students', __name__)

## INDEX
@students.route("/", methods=["GET"])
@jwt_required
def get_all_students():
    # payload= request.get_json()
    current_user_id = get_jwt_identity()
    try:
        students = [model_to_dict(student) for student in models.Student.select().where(models.Student.user == current_user_id )]
        return jsonify(data=students, status={"code": 200, "message": "Successfully retrieved students"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
          
    

## CREATE
@students.route("/", methods=["POST"])
@jwt_required
def create_student():
    payload = request.get_json()
    current_user_id = get_jwt_identity()
    try:
        student = models.Student.create(
            user=current_user_id,  # Associate the student with the logged-in user
            studentID=payload['studentID'],
            firstName=payload['firstName'],
            lastName=payload['lastName'],
            iep=payload['iep'],
            ell=payload['ell'],
            screenerScore=payload['screenerScore'],
            decodingScore=payload['decodingScore'],
            encodingScore=payload['encodingScore']
        )
        student_dict = model_to_dict(student)
        return jsonify(data=student_dict, status={"code": 201, "message": "Successfully created student"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})

        
## DELETE
@students.route("/<int:student_id>", methods=["DELETE"])
@login_required
def delete_student(student_id):
    try:
        student= models.Student.get((models.Student.id == student_id)& (models.Student.user == current_user))
        student.delete_instance()
        return jsonify(data={}, status={"code": 201, "message": "Successfully deleted student"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Student not found"})


## UPDATE
@students.route("/<int:student_id>", methods=["PUT"])
@login_required
def update_student(student_id):
    payload = request.get_json()
    try:
        student= models.Student.get((models.Student.id == student_id) & (models.Student.user == current_user))
        student.update(**payload).execute()
        updated_student = model_to_dict(update_student)
        student_dict = model_to_dict(update_student)
        return jsonify(data=student_dict, status={"code": 200, "message": "Student updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Student not found"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
