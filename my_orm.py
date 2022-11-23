from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import configparser


conf = configparser.ConfigParser()
conf.read('alembic.ini')
my_url = conf['alembic']['sqlalchemy.url']
engine = create_engine(my_url)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100))
    phone = Column(String(30))
    password = Column(String(200))
    UniqueConstraint(username, email)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __str__(self):
        return f'id: {self.id} name: {self.name}'

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100))
    password = Column(String(200))
    phone = Column(String(30))
    UniqueConstraint(username, email)


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True, autoincrement=True)
    studentId = Column(Integer, ForeignKey("student.id"))
    teacherId = Column(Integer, ForeignKey("teacher.id"))
    subjectId = Column(Integer, ForeignKey("subject.id"))
    score = Column(Integer, default=0)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200))
    password = Column(String(300))

    UniqueConstraint(username)