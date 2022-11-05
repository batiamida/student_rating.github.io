from flask import Flask, redirect, request, abort, jsonify
from flask_restful import Api, Resource
from waitress import serve
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, validate
import requests
from sqlalchemy.orm import scoped_session
from my_orm import Subject, Student, Score, Teacher, Session, Base
from my_tools import *
import json



app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)



class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True, validate=validate.Length(max=100))
    firstName = fields.Str(required=True, validate=validate.Length(max=50))
    lastName = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Str(required=True, validate=validate.Length(max=100))
    phone = fields.Str(required=True, validate=validate.Length(max=30))
    password = fields.Str(required=True, validate=validate.Length(max=50))

class ScoreSchema(Schema):
    id = fields.Int(required=True)
    studentId = fields.Int(required=True)
    teacherId = fields.Int(required=True)
    subjectId = fields.Int(required=True)
    score = fields.Int()

class SubjectSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class SubjectDeleteUpdateSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

user_schema = UserSchema()
score_schema = ScoreSchema()
subject_schema = SubjectSchema()
subject_du_schema = SubjectDeleteUpdateSchema()

@app.route('/')
def hello_world():
    return redirect('/hey', code=200)

@app.route('/hey')
def lab_func():
    return "Hello world 27"

@app.route('/student/<int:id>', methods=['GET'])
def getStudentById(id):
    return getById(Student, id)

class StudentResource(Resource):
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            abort(405, str(errors))
        else:
            phash = bcrypt.generate_password_hash(args.get('password'))
            student = Student()
            student.id = args.get('id')
            student.username = args.get('username')
            student.firstName = args.get('firstName')
            student.lastName = args.get('lastName')
            student.email = args.get('email')
            student.phone = args.get('phone')

            student.password = phash
            with Session() as session:
                session.add(student)
                session.commit()

        return 'ok'

    def get(self):
        return 0

    def put(self):
        pass


@app.route('/teacher/<int:id>', methods=['GET'])
def getTeacherById(id):
    return getById(Teacher, id)

class TeacherResource(Resource):
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            abort(405, str(errors))
        else:
            return args

    def get(self):
        pass

    def put(self):
        return {'data': 'hey'}

    def delete(self):
        pass


@app.route('/score/get_nrating', methods=['GET'])
def get_nrating(n):
    return n

@app.route('/score/<int:studentId>', methods=['GET'])
def getScoresByStudentId(studentId):
    kwargs = request.args
    instances = getBy(Score, studentId=studentId, **kwargs)
    ls = []
    for instance in instances:
        ls.append(score_schema.dump(instance))

    return jsonify(results=ls)

class ScoreResource(Resource):
    def post(self):

        return 'ok'

    def put(self):
        pass

    def delete(self):
        pass


@app.route('/subject/<int:id>', methods=['GET'])
def getSubjectById(id):
        return getById(Subject, id)

class SubjectResource(Resource):
    def post(self):
        args = request.args
        errors = subject_schema.validate(args)

        if errors:
            abort(405, str(errors))
        else:
            subject = Subject()
            subject.id = args.get('id')
            subject.name = args.get('name')
            create_object(subject)


        return 'ok'

    def delete(self):
        args = request.args
        errors = subject_du_schema.validate(args)
        if errors:
            abort(405, str(errors))
        else:
            id = args.get('id')
            deleteById(Subject, id)

        return 'ok'




api.add_resource(StudentResource, '/student')
api.add_resource(SubjectResource, '/subject')
# api.add_resource(Teacher, '/teacher/<int:id>', '/teacher')
api.add_resource(TeacherResource, '/teacher')


if __name__ == '__main__':
    app.run(debug=True)

else:
    serve(app, port=8080)

# if __name__ == '__main__':
#     print(requests.get('http://127.0.0.1:8080//teacher/1').json())
#     requests.post('http://127.0.0.1:5000//subject', params={'id': 4, 'name': 'sjsj'})