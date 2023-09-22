from peewee import *
import datetime
from flask_login import UserMixin
import os
from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///digitalliteracy.db')

class User(Model, UserMixin):
    username = CharField(unique=True)
    email = CharField(unique = True)
    password = CharField()
    
    class Meta:
        database = DATABASE

class Student(Model):
    user = ForeignKeyField(User, backref='students')  # Establishing the one-to-many relationship
    studentID = IntegerField(unique = True)
    firstName = CharField()
    lastName = CharField()
    iep = BooleanField(default=False)
    ell = BooleanField(default=False)
    screenerScore = IntegerField()
    decodingScore = IntegerField()
    encodingScore = IntegerField()
    
    class Meta:
        database = DATABASE
    
class PlacementCriteria(Model):
    user = ForeignKeyField(User, backref='placement_criteria')  # Establishing the one-to-many relationship
    interventionName = CharField(unique = True)
    screenerScoreMax = IntegerField()
    decodingScoreMax = IntegerField()
    encodingScoreMax = IntegerField()
    screenerScoreMin = IntegerField()
    decodingScoreMin = IntegerField()
    encodingScoreMin = IntegerField()
    
    class Meta:
        database = DATABASE
        
class PlacementMatch(Model):
    student = ForeignKeyField(Student)
    intervention = CharField()
    score_difference = IntegerField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    # DATABASE.drop_tables([User, PlacementCriteria, Student], safe=True)

    DATABASE.create_tables([User, PlacementCriteria, Student, PlacementMatch], safe=True)
    print("Connected to the database, tables created.")
    DATABASE.close()