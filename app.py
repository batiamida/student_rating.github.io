from flask import Flask, redirect, request, abort, jsonify
from flask_restful import Api, Resource
from waitress import serve
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, validate
import requests
from my_orm import Subject, Student, Score, Teacher, Session, Base
from my_tools import *
import json
from flask import Response


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)


def custom_response(status_code, error):
    return Response(error, status=status_code, mimetype='application/json')


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(max=100))
    firstName = fields.Str(required=True, validate=validate.Length(max=50))
    lastName = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True, validate=validate.Length(max=100))
    phone = fields.Str(required=True, validate=validate.Length(max=30))
    password = fields.Str(required=True, validate=validate.Length(max=100))

class UserDeleteUpdateSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(validate=validate.Length(max=100))
    firstName = fields.Str(validate=validate.Length(max=50))
    lastName = fields.Str(validate=validate.Length(max=50))
    email = fields.Str(validate=validate.Length(max=100))
    phone = fields.Str(validate=validate.Length(max=30))
    password = fields.Str(validate=validate.Length(max=200))

class ScoreSchema(Schema):
    id = fields.Int()
    studentId = fields.Int(required=True)
    teacherId = fields.Int(required=True)
    subjectId = fields.Int(required=True)
    score = fields.Int()

class ScoreDeleteUpdateSchema(Schema):
    id = fields.Int(required=True)
    score = fields.Int()

class SubjectSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

class SubjectDeleteUpdateSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()

class RatingSchema(Schema):
    n = fields.Int()

user_schema = UserSchema()
score_schema = ScoreSchema()
score_du_schema = ScoreDeleteUpdateSchema()
subject_schema = SubjectSchema()
subject_du_schema = SubjectDeleteUpdateSchema()
rating_schema = RatingSchema()
user_du_schema = UserDeleteUpdateSchema()

@app.route('/')
def hello_world():
    return redirect('/hey', code=200)

@app.route('/api/v1/hello-world-27')
def lab_func():
    return "Hello world 27"

@app.route('/student/<int:id>', methods=['GET'])
def getStudentById(id):
    if getById(Student, id) != None:
        return user_schema.dump(getById(Student, id))
    else:
        return custom_response(404, 'student not found')

class StudentResource(Resource):
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            return custom_response(405, errors)
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
            if create_object(student):
                return 'ok'
            else:
                return custom_response(405, 'student already exists')




    def put(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(405, str(errors))
        else:
            if updateById(Student, **args):
                return 'ok'
            else:
                return custom_response(404, 'student not found')

    # return 'ok'

    def delete(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            # print(type(args.get('id')))
            response = deleteById(Student, int(args.get('id')))
            if response == 1:
                return 'ok'
            elif response == 2:
                return custom_response(500, 'foreign key restriction')
            else:
                return custom_response(404, 'student not found')


@app.route('/teacher/<int:id>', methods=['GET'])
def getTeacherById(id):
    result = getById(Teacher, id)
    if result != None:
        print(user_schema.dump(result))
        return user_schema.dump(result)
    else:
        return custom_response(404, 'teacher not found')

class TeacherResource(Resource):
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            return str(errors)
        else:
            phash = bcrypt.generate_password_hash(args.get('password'))
            teacher = Teacher()
            teacher.id = args.get('id')
            teacher.username = args.get('username')
            teacher.firstName = args.get('firstName')
            teacher.lastName = args.get('lastName')
            teacher.email = args.get('email')
            teacher.phone = args.get('phone')
            teacher.password = phash
            if create_object(teacher):
                return "ok"
            else:
                return custom_response(405, 'teacher already exists')





    def put(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(405, str(errors))
        else:
            if updateById(Teacher, **args):
                return 'ok'
            else:
                return custom_response(404, 'teacher not found')



    def delete(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            response = deleteById(Student, int(args.get('id')))
            if response == 1:
                return 'ok'
            elif response == 2:
                return custom_response(500, 'foreign key restriction')
            else:
                return custom_response(404, 'teacher not found')


@app.route('/score/<int:n>', methods=['GET'])
def get_nrating(n):


    d = {}
    instances = getAllStudents()
    print(instances)
    for instance in instances:
        student = user_schema.dump(instance)
        scores = getScoresByStudentId(student['id']).get_json()['results']
        my_key = f'{student["username"]} {student["firstName"]} {student["lastName"]} {student["email"]}'
        d[my_key] = {'rating': 0}

        for score in scores:
            d[my_key]['rating'] += score['score']

        if len(scores) > 0:
            d[my_key]['rating'] /= len(scores)

    return sorted(d, key=lambda x: d[x]['rating'], reverse=True)[:n]


@app.route('/score/<int:studentId>', methods=['GET'])
def getScoresByStudentId(studentId):
    kwargs = request.args
    instances = getBy(Score, studentId=studentId, **kwargs)
    ls = []
    if instances:
        for instance in instances:
            ls.append(score_schema.dump(instance))

        return jsonify(results=ls)
    else:
        return custom_response(404, 'Scores are not found')

class ScoreResource(Resource):
    def post(self):
        args = request.args
        errors = score_schema.validate(args)

        if errors:
            return str(errors)
        else:
            score = Score()
            score.id = args.get('id')
            score.subjectId = args.get('subjectId')
            score.teacherId = args.get('teacherId')
            score.studentId = args.get('studentId')
            score.score = args.get('score')

            if create_object(score):
                return "ok"
            else:
                return custom_response(405, 'score already exists')

    def put(self):
        args = request.args
        errors = score_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            updateById(Score, args.get('id'), score=args.get('score'))

        return 'ok'



    def delete(self):
        args = request.args
        errors = score_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            response = deleteById(Student, int(args.get('id')))
            if response == 1:
                return 'ok'
            elif response == 2:
                return custom_response(500, 'foreign key restriction')
            else:
                return custom_response(404, 'score not found')


@app.route('/subject/<int:id>', methods=['GET'])
def getSubjectById(id):
    result = getById(Subject, id)
    if result != None:
        print(subject_schema.dump(result))
        return subject_schema.dump(result)
    else:
        return custom_response(404, 'subject not found')

class SubjectResource(Resource):
    def post(self):
        args = request.args
        errors = subject_schema.validate(args)

        if errors:
            return str(errors)
        else:
            subject = Subject()
            subject.id = args.get('id')
            subject.name = args.get('name')

            if create_object(subject):
                return "ok"

            else:
                return custom_response(404, 'Subject already exists')


    def delete(self):
        args = request.args
        errors = subject_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            response = deleteById(Student, int(args.get('id')))
            if response == 1:
                return 'ok'
            elif response == 2:
                return custom_response(500, 'foreign key restriction')
            else:
                return custom_response(404, 'subject not found')





api.add_resource(StudentResource, '/student')
api.add_resource(SubjectResource, '/subject')
api.add_resource(TeacherResource, '/teacher')
api.add_resource(ScoreResource, '/score')


if __name__ == '__main__':
    app.run(debug=True)

else:
    serve(app, port=8080)

# if __name__ == '__main__':
#     print(requests.get('http://127.0.0.1:8080//teacher/1').json())
#     requests.post('http://127.0.0.1:5000//teacher', params={'username': 'SomeUsername', 'email': 'someemail', 'password': 'somepass', 'phone':'3341'})