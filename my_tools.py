from my_orm import Session

def deleteById(model, id):
    with Session() as session:
        session.query(model).filter_by(id=id).delete()
        session.commit()


def create_object(instance):
    with Session() as session:
        session.add(instance)
        session.commit()


def getById(model, id):
    with Session() as session:
        result = session.query(model).filter_by(id=id).one()

    return result

def getBy(model, **kwargs):
    with Session() as session:
        results = session.query(model).filter_by(**kwargs).all()

    return results


def updateById(model, id, **kwargs):
    with Session() as session:
        instance = getById(model, id)
        instance(**kwargs)
        session.commit()



