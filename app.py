from flask import Flask, redirect, request, abort, jsonify, session, make_response
from flask_restful import Api, Resource
from waitress import serve
from flask_bcrypt import Bcrypt
from flask import Response
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, validate
import requests
from my_orm import Subject, Student, Score, Teacher, Session, Base, Admin
from my_tools import *
import json

from flask_cors import cross_origin



app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()
app.secret_key = 'hello'

def student_required(f):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return custom_response(403, "Access denied")
        results = getBy(Student, username=auth.username)
        if len(results) > 0 or len(getBy(Admin, username=auth.username)) > 0:
            if getOneBy(Student, username=auth.username) is None:
                session['admin'] = 1
                session['id'] = 1
            else:
                session['admin'] = 0
                session['id'] = results[0].id

            return f(*args, **kwargs)
        else:
            return custom_response(403, "Access denied")

    return wrapper

def teacher_required(f):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return custom_response(403, "Access denied")
        results = getBy(Teacher, username=auth.username)
        admin_results = getBy(Admin, username=auth.username)
        if (len(results) > 0) or (len(admin_results) > 0):
            if getOneBy(Teacher, username=auth.username) is None:
                session['admin'] = 1
                session['id'] = 1
            else:
                session['admin'] = 0
                session['id'] = results[0].id

            return f(*args, **kwargs)
        else:
            return custom_response(403, "Access denied")

    return wrapper


def admin_required(f):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return custom_response(403, "Access denied")
        results = getBy(Admin, username=auth.username)
        if len(results) > 0:
            return f(*args, **kwargs)
        else:
            return custom_response(403, "Access denied")

    return wrapper

@auth.verify_password
def verify(username, password):
    if not(username and password):
        return False

    phash = checkEveryoneBy(username=username)
    if phash:
        phash = phash[1].password
        return bcrypt.check_password_hash(phash, password)



# @app.route('/login', methods=['GET'])
# @auth.login_required
# def login():
#     return jsonify({"status": True})

# @app.route('/logout', methods=['GET'])
# def logout():
#     return jsonify({"Status": True})


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
    return redirect('/api/v1/hello-world-27', code=200)

@app.route('/api/v1/hello-world-27')
def lab_func():
    return "Hello world 27"

@app.route('/user_listing', methods=['GET'])
@cross_origin()
def getUsers():
    # print('smth')
    ls = []
    for user in getAllUsers():
        ls.append({"name": user[1], "firstName": user[2], "lastName": user[3], "email": user[-1]})
        # d[user[1]] = d[user[]]
    # print(make_response(ls).json)
    return make_response(ls)


@app.route('/student/<int:id>', methods=['GET'])
def getStudentById(id):
    if getById(Student, id) != None:
        r = user_schema.dump(getById(Student, id))
        r["role"] = "student"
        r = make_response(r)
        r.headers.add('Access-Control-Allow-Origin', '*')
        return r
    else:
        return custom_response(404, 'student not found')

class StudentResource(Resource):
    @teacher_required
    @auth.login_required
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            return custom_response(405, errors)
        else:
            phash = bcrypt.generate_password_hash(args.get('password')).decode('utf-8')
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



    @student_required
    @auth.login_required
    def put(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(405, str(errors))
        else:
            if session['id'] == int(args['id']) or session['admin'] == 1:
                if updateById(Student, **args):
                    return 'ok'
                else:
                    return custom_response(404, 'student not found')
            else:
                return custom_response(403, 'access denied')


    # return 'ok'

    @student_required
    @auth.login_required
    def delete(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(500, errors)
        else:
            # print(type(args.get('id')))
            if session['id'] == int(args['id']) or session['admin'] == 1:
                response = deleteById(Student, int(args.get('id')))
                if response == 1:
                    return 'ok'
                elif response == 2:
                    return custom_response(500, 'foreign key restriction')
                else:
                    return custom_response(404, 'student not found')
            else:
                return custom_response(403, 'access denied')




@app.route('/teacher/<int:id>', methods=['GET'])
def getTeacherById(id):
    result = getById(Teacher, id)
    if result != None:
        return user_schema.dump(result)
    else:
        return custom_response(404, 'teacher not found')

class TeacherResource(Resource):
    @admin_required
    @auth.login_required
    def post(self):
        args = request.args
        errors = user_schema.validate(args)

        if errors:
            return custom_response(500, errors)
        else:
            phash = bcrypt.generate_password_hash(args.get('password')).decode('utf-8')
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




    @teacher_required
    @auth.login_required
    def put(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(500, str(errors))
        else:
            if session['id'] == int(args['id']) or session['admin'] == 1:
                if updateById(Teacher, **args):
                    return 'ok'
                else:
                    return custom_response(404, 'teacher not found')
            else:
                return custom_response(403, 'access denied')





    @teacher_required
    @auth.login_required
    def delete(self):
        args = request.args
        errors = user_du_schema.validate(args)

        if errors:
            return custom_response(500, str(errors))
        else:
            if session['id'] == int(args['id']) or session['admin'] == 1:
                response = deleteById(Teacher, int(args.get('id')))
                if response == 1:
                    return 'ok'
                elif response == 2:
                    return custom_response(500, 'foreign key restriction')
                else:
                    return custom_response(404, 'teacher not found')
            else:
                return custom_response(403, 'Access denied')



@app.route('/score/rating/<int:n>', methods=['GET'])
@cross_origin()
def get_nrating(n):
    d = {}
    instances = getAllStudents()
    result = []
    for instance in instances:
        student = user_schema.dump(instance)
        if getBy(Score, studentId=student['id']):
            scores = getScoresByStudentId(student['id']).get_json()['results']
            my_key = f'{student["username"]} {student["email"]}'

            d[my_key] = {}

            for score in scores:
                subject = getSubjectById(id=score["subjectId"]).get("name")
                if d[my_key].get(subject) is not None:
                    d[my_key][subject]['rating'] += score['score']
                else:
                    d[my_key][subject] = {}
                    d[my_key][subject]['rating'] = 0
                # d[my_key]["subject"] = subject
    
    result = []
    for key, val in d.items():
        result.append({"name": key.strip().split()[0], "scores": val})

    print(result)
                # print(sorted(d[my_key], key=lambda x: d[x]['rating'], reverse=True)[:n])
    # return sorted(d, key=lambda x: d[x]['rating'], reverse=True)[:n]
    # print(d)
    # sorted_list = sorted(d, key=lambda x, y: d[x][y]['rating'], reverse=True)[:n]
    # result = []
    # print(sorted_list)
    # for item in sorted_list:
    #     user_name, _ = item.strip().split()
    #     result.append({"name": user_name, "rating": d[item]['rating'],
    #      d[item]["subject"]})
    
    # return jsonify(result)
    return jsonify(result)


@app.route('/score/<int:studentId>', methods=['GET'])
@cross_origin()
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
    @teacher_required
    @auth.login_required
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

            resp = create_object(score)
            if resp == 1:
                return "ok"

            elif resp == 2:
                return custom_response(500, 'minus score')

            elif resp == 3:
                return custom_response(500, 'foreign key restriction')
            else:
                return custom_response(405, 'score already exists')

    @teacher_required
    @auth.login_required
    def put(self):
        args = request.args
        errors = score_du_schema.validate(args)

        if errors:
            return custom_response(500, str(errors))
        else:
            if args.get('score') is not None and int(args.get('score')) < 0:
                return custom_response(500, 'minus score')

            else:
                if updateById(Score, **args):
                    return 'ok'
                else:
                    return custom_response(404, 'score not found')


    @teacher_required
    @auth.login_required
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
        return subject_schema.dump(result)
    else:
        return custom_response(404, 'subject not found')

class SubjectResource(Resource):
    @teacher_required
    @auth.login_required
    def post(self):
        args = request.args
        errors = subject_schema.validate(args)

        if errors:
            return custom_response(500, str(errors))
        else:
            subject = Subject()
            subject.id = args.get('id')
            subject.name = args.get('name')

            if create_object(subject):
                return "ok"

            else:
                return custom_response(404, 'Subject already exists')

    @teacher_required
    @auth.login_required
    def delete(self):
        args = request.args
        errors = subject_du_schema.validate(args)

        if errors:
            return custom_response(500, str(errors))
        else:
            response = deleteById(Subject, int(args.get('id')))
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