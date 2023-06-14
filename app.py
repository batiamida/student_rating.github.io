from flask import Flask, redirect, request, abort, jsonify, session, make_response
from flask_restful import Api, Resource
from waitress import serve
from flask_bcrypt import Bcrypt
from flask import Response
import functools
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import sessionmaker
from marshmallow import Schema, fields, validate
import requests
from my_orm import Subject, Student, Score, Teacher, Session, Base, Admin
from my_tools import *
import json
from datetime import timedelta, datetime, timezone

from flask_cors import cross_origin

from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, decode_token as jwt_decode
# import jwt as jwt_extended
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

api = Api(app)
CORS(app, origins=["http://localhost:3000"])
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
# auth = HTTPBasicAuth()
# app.secret_key = 'hello'

def decode_token(token):
    try:
        # options = {'verify_aud': False, 'require_sub': True}

        # print(dir(jwt_extended))
        decoded = jwt_decode(token)
        print(decoded, "decoded")
        return decoded
    except Exception as e:
        print(e)
        return None, None

def student_required(f):
    def wrapper(*args, **kwargs):
        # print("auth", request.headers.get("Authorization").split(" ")[1])
        token = request.headers.get("Authorization").split(" ")[1]
        auth = decode_token(token)
        print(auth)
        print("auth", auth)
        # print("auth", auth)
        # print(dir(request), request.get_json())
        if auth is None:
            # print("auth", auth)
            return custom_response(403, "Access denied")
        result = getOneBy(Student, username=auth.get("sub"))
        if result is not None or getOneBy(Admin, username=auth.get("sub")) is not None:
        # if len(results) > 0 or len(getBy(Admin, username=auth.get("sub"))) > 0:
        #     if getOneBy(Student, username=auth.get("sub")) is None:
            #     session['admin'] = 1
            #     session['id'] = 1
            # else:
            #     session['admin'] = 0
            #     session['id'] = results[0].id

            return f(*args, **kwargs)
        else:
            return custom_response(403, "Access denied")

    return wrapper


def teacher_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization").split(" ")[1]
        auth = decode_token(token)
        print(auth)
        if auth is None:
            return custom_response(403, "Access denied")
        result = getBy(Teacher, username=auth.get("sub"))
        print(result)
        admin_result = getBy(Admin, username=auth.get("sub"))
        if len(result) > 0 or len(admin_result) > 0:
        # if (len(results) > 0) or (len(admin_results) > 0):
        #     if getOneBy(Teacher, username=auth.username) is None:
        #         session['admin'] = 1
        #         session['id'] = 1
        #     else:
        #         session['admin'] = 0
        #
        #         session['id'] = results[0].id
        #     return custom_response(403, "access denied")
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

# @auth.verify_password
def verify(username, password):
    if not(username and password):
        return False

    phash = checkEveryoneBy(username=username)
    if phash:
        phash = phash[1].password
        return bcrypt.check_password_hash(phash, password)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route("/logout", methods=["POST"])
@cross_origin()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/token", methods=["POST"])
@cross_origin()
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not verify(username, password):
        return {"msg": "Wrong username or password"}, 401

    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}
    return response

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

@app.route('/get_auth_user', methods=['GET'])
@cross_origin()
@jwt_required()
def getAuthUser():
    current_user = get_jwt_identity()
    found_model, model = checkEveryoneBy(username=current_user)
    d = {}
    if found_model:
        # print(dir(model))
        for col in ["email", "firstName", "lastName", "username"]:
            # print(f"d['{col}']=model.{col}")
            exec(f"d['{col}']=model.{col}")

            # d[col] =
    d["model"] = model.__class__.__name__
    # print(d)
    # print(d)
    return jsonify(user=d), 200

@app.route('/user_listing', methods=['GET'])
@cross_origin()
def getUsers():
    # print('smth')
    ls = []
    for user in getAllUsers():
        print(user)
        ls.append({"id": user[0], "name": user[1], "firstName": user[2], "lastName": user[3], "email": user[-1]})
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
    @jwt_required()
    def post(self):
        args = request.get_json()
        print(args)
        errors = user_schema.validate(args)
        print(errors)
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
    @jwt_required()
    def put(self):
        # args = request.get_json()
        args = getAuthUser().get_json()["user"]
        print(args)
        # print(getOneBy(Student, getAuthUser().get_json()["user"]))
        del args["model"]
        # print(smth)
        user = getOneBy(Student, **args)
        args["id"] = user.id

        # print(user)
        # print(args)
        errors = user_du_schema.validate(args)
        token = request.headers.get('Authorization').split(' ')[1]
        auth = decode_token(token)
        # is_admin = getBy(Admin, username=username) is None
        # print(user_id, is_admin)
        if auth is None:
            return custom_response(401, 'Invalid token')
        elif errors:
            print(errors)
            return custom_response(405, str(errors))

        else:
            # if is_admin:
            args = request.get_json()
            # print(args)
            args["id"] = user.id
            del args["model"]
            if updateById(Student, **args):
                access_token = create_access_token(identity=args.get("username"))
                response = {"token": access_token}
                # print(new_token)
                return response
                # return 'ok'
            else:
                return custom_response(404, 'student not found')
            # else:
            # return custom_response(403, 'access denied')


    # return 'ok'

    @student_required
    @jwt_required()
    def delete(self):
        args = getAuthUser().get_json()["user"]
        # print(args)
        del args["model"]
        user = getOneBy(Student, **args)
        args["id"] = user.id
        print(args)
        errors = user_du_schema.validate(args)
        print(errors)
        if errors:
            return custom_response(500, errors)
        else:
            # print(type(args.get('id')))
            # if session['id'] == int(args['id']) or session['admin'] == 1:
            response = deleteById(Student, int(args.get('id')))
            if response == 1:
                return 'ok'
            elif response == 2:
                # print("not found")
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
    @jwt_required()
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
    @jwt_required()
    def put(self):
        args = request.get_json()
        del args["model"]
        errors = user_du_schema.validate(args)

        args = getAuthUser().get_json()["user"]
        print(args)
        # print(getOneBy(Student, getAuthUser().get_json()["user"]))
        del args["model"]
        # print(smth)
        user = getOneBy(Teacher, **args)
        args["id"] = user.id

        if errors:
            return custom_response(500, str(errors))
        else:
            if session['id'] == int(args['id']) or session['admin'] == 1:
                args = request.get_json()
                # print(args)
                args["id"] = user.id
                del args["model"]
                if updateById(Teacher, **args):
                    return 'ok'
                else:
                    return custom_response(404, 'teacher not found')
            else:
                return custom_response(403, 'access denied')





    @teacher_required
    @jwt_required()
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
                    d[my_key][subject]['rating'] = score.get("score", 0)
                # d[my_key]["subject"] = subject
    result = []
    for name, val in d.items():
        for key, score in val.items():
            result.append({
                "name": name.strip().split()[0],
                "score": {
                    "name": key.capitalize(),
                    "value": score["rating"]
                }
            })

    # result.sort(key=lambda x: x["score"]["value"], reverse=True)
    df = pd.DataFrame(result)
    df["subject"] = df["score"].apply(lambda x: [x["name"], x["value"]][0])
    df["score"] = df["score"].apply(lambda x: [x["name"], x["value"]][1])
    result = []
    for group in df.groupby("subject"):
        # print(group[1])
        for score in group[1].sort_values(by="score", ascending=False).values[:n]:
            d = {}
            d["name"] = score[0]
            d["score"] = {"name": score[2], "value": score[1]}
            result.append(d)

    # print(df)
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
            # print(ls)

        return jsonify(results=ls)
    else:
        return custom_response(404, 'Scores are not found')

@app.route('/scores/<int:studentId>', methods=['GET'])
def getScoresByStudentIdPrettify(studentId):
    scores = getScoresByStudentId(studentId).get_json()["results"]
    ls = []
    for score in scores:
        # print(score)
        subject = subject_schema.dump(getOneBy(Subject, id=score["subjectId"]))
        teacher = user_schema.dump(getOneBy(Teacher, id=score["teacherId"]))
        d = {"teacher_id": score["teacherId"], "subject_id": score["subjectId"],
             "teacher": teacher, "subject": subject, "score": score["score"], "id": score["id"]}
        # print(score)
        ls.append(d)
        # print(subject_schema.dump(subject)
        # print(subject)
        # print(score["subjectId"])
    # subject = scores_temp["subjectId"]
    # print(scores_temp)

    return jsonify(ls)
# @teacher_required

@app.route('/score_value', methods=['PUT'])
def update_score_value_by_id():
    score = request.get_json()
    updateById(Score, id=score["id"], score=score["value"])

    return {"smth": "snsn"}



class ScoreResource(Resource):
    @teacher_required
    @jwt_required()
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
    @jwt_required()
    def put(self):
        args = request.get_json()
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
    @jwt_required()
    def delete(self):
        args = request.get_json()
        errors = score_du_schema.validate(args)

        if errors:
            return str(errors)
        else:
            response = deleteById(Score, int(args.get('id')))
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

@app.route('/subjects_and_teachers', methods=["GET"])
@teacher_required
@jwt_required()
def get_subjects_and_teachers():
    subjects = getAllSubjects()
    teachers = getAllTeachers()
    ls_teacher = []
    ls_subject = []

    for teacher in teachers:
        d = {}
        for key, val in zip(["id", "username", "firstName", "lastName", "email"], teacher):
            d[key] = val
        ls_teacher.append(d)

    for subject in subjects:
        d = {}
        for key, val in zip(["id", "name"], subject):
            d[key] = val
        ls_subject.append(d)

    return jsonify({"teachers": ls_teacher, "subjects": ls_subject})




@app.route('/score_by_names', methods=["POST"])
@teacher_required
@jwt_required()
def score_by_names():
    kwargs = request.get_json()
    teacher = getOneBy(Teacher, username=kwargs.get("teacher_name"))
    subject = getOneBy(Subject, name=kwargs.get("subject_name"))
    kwargs = {"subjectId": subject.id,
            "studentId": kwargs.get("student_id"),
            "teacherId": teacher.id, "score": kwargs.get("score")}

    errors = score_schema.validate(kwargs)

    if errors:
        return custom_response(500, str(errors))

    score = Score()
    score.studentId = kwargs.get("studentId")
    score.teacherId = kwargs.get("teacherId")
    score.subjectId = kwargs.get("subjectId")
    score.score = kwargs.get("score")
    if create_object(score) == 1:
        return custom_response(200, "succesfully created")

    return custom_response(500, "constraints")

class SubjectResource(Resource):
    @teacher_required
    @jwt_required()
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
    @jwt_required()
    def delete(self):
        args = request.args
        errors = subject_du_schema.validate(args)
        print(args)
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