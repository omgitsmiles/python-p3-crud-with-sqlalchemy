#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthdate = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: "\
            + f"{self.name}, " \
            + f"Grade {self.grade}" 

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthdate=datetime(
            1879, 
            3, 
            14),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthdate=datetime(
            1912,
            6,
            23),
    )

# create
    
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

# read

    names = session.query(Student.name).order_by(Student.name).all()
    print(names)

    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11).all()
    
    for rec in query:
        print(rec)

# update

    for student in session.query(Student):
        student.grade += 1
    
    session.commit()

    print([(student.name, student.grade) for student in session.query(Student)])

    session.query(Student).update({
        Student.grade: (Student.grade + 1)
    })

    print([(student.name, student.grade) for student in session.query(Student)])

# delete

query = session.query(Student).filter(
    Student.name == "Albert Einstein")

albert_einstein = query.first()

# or

query.delete()

session.delete(albert_einstein)
session.commit()


