from my_orm import Session, Student
from sqlalchemy.orm import load_only
from flask import jsonify

def deleteAll():
    with Session() as session:
        session.execute('DELETE FROM score *')
        session.commit()
        session.execute('DELETE FROM student *')
        session.commit()
        session.execute('DELETE FROM teacher *')
        session.commit()
        session.execute('DELETE FROM subject *')
        session.commit()

def deleteById(model, id):
    with Session() as session:
        instance = session.query(model).filter_by(id=id)
        # print(instance.first())
        if instance.first() != None:
            instance.delete()
            session.commit()
            session.execute(f'ALTER SUEQNCE {instance.__tablename__}_id_seq RESTART WITH {id-1}')
            return 1
        else:
            return 0







def getById(model, id):
    with Session() as session:
        result = session.query(model).filter_by(id=id).first()

    return result

def create_object(instance):
    with Session() as session:
         result = session.query(instance.__class__).first()
        # # print(result)
        # result = None
         if result==None:
            session.add(instance)
            session.commit()
            return 1
         else:
            return 0

def getBy(model, **kwargs):
    with Session() as session:
        results = session.query(model).filter_by(**kwargs).all()

    return results


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
        results = session.query(Student).with_entities(Student.id, Student.username).all()
    return results

def restart_all_seq():
    with Session() as session:
        session.execute('ALTER SEQUENCE teacher_id_seq RESTART WITH 1')
        session.execute('ALTER SEQUENCE student_id_seq RESTART WITH 1')
        session.execute('ALTER SEQUENCE subject_id_seq RESTART WITH 1')
        session.execute('ALTER SEQUENCE score_id_seq RESTART WITH 1')
        session.commit()
