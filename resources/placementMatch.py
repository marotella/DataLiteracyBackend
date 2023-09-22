from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from peewee import fn
from models import Student, PlacementCriteria, PlacementMatch

match = Blueprint('placement', __name__)

