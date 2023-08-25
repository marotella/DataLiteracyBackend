from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import models

students = Blueprint('students', __name__)

## INDEX
@students.route("/students", methods=["GET"])
@login_required
def get_all_studnets():
    payload= request.get_json()
    try:
        students = [model_to_dict(student) for student in current_user.students]
        return jsonify(data=students, status={"code": 200, "message": "Successfully retrieved students"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})
        
    
    
    

## NEW
@students.route("/students", methods=["POST"])
@login_required
def create_studnet():
    payload = request.get_json()
    try:
        student = models.Student.create(
            studentID=payload['studentID']
            firstName=payload['firstName'],
            lastName=payload['lastName'],
            iep=payload['iep'],
            ell=payload['ell'],
            screenerScore=payload['screenerScore'],
            decodingScore=payload['decodingScore'],
            encodingScore=payload['encodingScore']
        )
        student_dict = model_to_dict(student)
        return jsonify(data=student_dict, status={"code": "201", "message": "Successfully created student"})
    except Exception as e:
        return jsonify(data={}, status={"code": 400, "message": str(e)})

        
## DELETE
@students.route("/student/<int:student_id>", methods=["DELETE"])
@login_required
def delete_student(student_id):
    try:
        student= models.Student.get((models.Student.id == student_id)& (models.Student.user == current_user))
        student.delete_instance()
        return jsonify(data={}, status={"code": "201", "message": "Successfully deleted student"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 404, "message": "Student not found"})


## UPDATE

## CREATE

## EDIT