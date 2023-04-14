from my_orm import Session, Student, Teacher, Subject, Admin
from sqlalchemy.orm import load_only
from flask import jsonify





def deleteById(model, id):
    with Session() as session:
        instance = session.query(model).filter_by(id=id)
        # print(instance.first())
        try:
            if instance.first() != None:
                instance.delete()
                session.commit()
                return 1
            else:
                return 0
        except:
            return 2



def getById(model, id):
    with Session() as session:
        result = session.query(model).filter_by(id=id).first()

    return result

def create_object(instance):
    with Session() as session:
        class_name = instance.__class__.__name__
        my_query = None
        if class_name == 'Teacher' or class_name == 'Student':
            my_query = session.query(instance.__class__).filter_by(username=instance.username,
                                                                    email=instance.email).first()
        elif class_name == 'Subject':
            my_query = session.query(instance.__class__).filter_by(name=instance.name).first()

        elif class_name == 'Score':
            my_query = session.query(instance.__class__).filter_by(studentId=instance.studentId,
                                                                   teacherId=instance.teacherId,
                                                                   subjectId=instance.subjectId).first()
            student_query = session.query(Student).filter_by(id=instance.studentId).first()
            teacher_query = session.query(Teacher).filter_by(id=instance.teacherId).first()
            subject_query = session.query(Subject).filter_by(id=instance.subjectId).first()

            if instance.score is not None:
                if int(instance.score) < 0:
                    return 2

            temp_f = lambda x: x is None

            if any(map(temp_f, [student_query, teacher_query, subject_query])):
                return 3



        if my_query == None:
            session.add(instance)
            session.commit()
            return 1
        else:
            return 0

def getBy(model, **kwargs):
    with Session() as session:
        results = session.query(model).filter_by(**kwargs).all()

    return results

def getOneBy(model, **kwargs):
    with Session() as session:
        result = session.query(model).filter_by(**kwargs).first()

    return result

def checkEveryoneBy(**kwargs):
    result = None
    with Session() as session:
        models = [Admin, Student, Teacher]
        for model in models:
            if session.query(model).filter_by(**kwargs).first() is not None:
                result = session.query(model).filter_by(**kwargs).first()

    return 0 if result is None else (1, result)


def updateById(model, id, **kwargs):
    with Session() as session:
        instance = session.query(model).filter_by(id=id).first()
        if instance != None:
            for key, value in kwargs.items():
                exec(f'instance.{key} = value')
            session.commit()

            return True
    return False

        # result = model.__tablename__ + " not found"
        #     return result

def getAllStudents():
    with Session() as session:
        results = session.query(Student).with_entities(Student.id, Student.username,
                                                        Student.firstName, Student.lastName,
                                                       Student.email).all()
    return results
def getAllTeachers():
    with Session() as session:
        results = session.query(Teacher).with_entities(Teacher.id, Teacher.username, Teacher.firstName, Teacher.lastName, Teacher.email).all()

    return results

def getAllUsers():
    students = getAllStudents()
    teachers = getAllTeachers()    

    return [*students, *teachers]

# def deleteAll():
#     with Session() as session:
#         session.execute('DELETE FROM score *')
#         session.commit()
#         session.execute('DELETE FROM student *')
#         session.commit()
#         session.execute('DELETE FROM teacher *')
#         session.commit()
#         session.execute('DELETE FROM subject *')
#         session.commit()
#

# def restart_all_seq():
#     with Session() as session:
#         session.execute('ALTER SEQUENCE teacher_id_seq RESTART WITH 1')
#         session.execute('ALTER SEQUENCE student_id_seq RESTART WITH 1')
#         session.execute('ALTER SEQUENCE subject_id_seq RESTART WITH 1')
#         session.execute('ALTER SEQUENCE score_id_seq RESTART WITH 1')
#         session.commit()


