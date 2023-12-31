from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import models

students = Blueprint('students', __name__)

## INDEX
@students.route("/", methods=["GET"])
@jwt_required()
def get_all_students():
    current_user_id = get_jwt_identity()
    token = request.headers.get("Authorization")  # Get the token from the Authorization header
    print(f"Token: {token}")
    print(f"Current User ID: {current_user_id}")
    try:
        students = [model_to_dict(student) for student in models.Student.select().where(models.Student.user == current_user_id )]
        print(students)
        return jsonify(data=students, status={"code": 200, "message": "Successfully retrieved students"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
          
    

## CREATE
@students.route("/create", methods=["POST"])
@jwt_required()
def create_student():
    current_user_id = get_jwt_identity()
    token = request.headers.get("Authorization")  # Get the token from the Authorization header
    print(f"Token: {token}")
    try:
        payload = request.get_json()
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
        print(student)
        student_dict = model_to_dict(student)
        return jsonify(data=student_dict, status={"code": 201, "message": "Successfully created student"})
    except KeyError as e:
        return jsonify(data={}, status={"code": 400, "message": f"Missing required field: {e}"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})

        
## DELETE
@students.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
def delete_student(student_id):
    current_user_id = get_jwt_identity()
    try:
        student= models.Student.get((models.Student.id == student_id)& (models.Student.user == current_user_id))
        student.delete_instance()
        return jsonify(data={}, status={"code": 201, "message": "Successfully deleted student"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Student not found"})


## UPDATE
@students.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    payload = request.get_json()
    current_user_id = get_jwt_identity()
    try:
        student= models.Student.get((models.Student.id == student_id) & (models.Student.user == current_user_id))
        student.update(**payload).execute()
        updated_student = model_to_dict(student)
        return jsonify(data=updated_student, status={"code": 200, "message": "Student updated"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Student not found"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
