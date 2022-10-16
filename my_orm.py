from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100))
    phone = Column(String(30))
    password = Column(String(50))


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))



class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    password = Column(String(100))


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    studentId = Column(Integer, ForeignKey("student.id"))
    teacherId = Column(Integer, ForeignKey("teacher.id"))
    subjectId = Column(Integer, ForeignKey("subject.id"))
    score = Column(Integer)

