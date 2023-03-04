import faker
from faker.providers import DynamicProvider
import pathlib
import configparser
from connector import session
from sqlalchemy import select
from db_models import Teacher, Student, Subject, Group, Journal
from random import randint, choice

file_ini = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_ini)

NUMBER_GROUP = int(config.get('SEED', 'NUMBER_GROUP'))
NUMBER_STUDENTS = int(config.get('SEED', 'NUMBER_STUDENTS'))
NUMBER_TEACHERS = int(config.get('SEED', 'NUMBER_TEACHERS'))
NUMBER_SUBJECT = int(config.get('SEED', 'NUMBER_SUBJECT'))


def fill_db():
    """generate some fake lists"""

    fake_data = faker.Faker()

    for _ in range(0, NUMBER_TEACHERS):
        teacher = Teacher(full_name=fake_data.name())
        session.add(teacher)
    session.commit()

    subject_provider = DynamicProvider(
        provider_name="subject",
        elements=["Computer Science", "Computing", "IT", "Multimedia", "Software", "Architecture", "Built Environment",
                  "Construction", "Maintenance Services", "Planning", "Property Management", "Surveying"],
    )
    fake_data.add_provider(subject_provider)
    ids_teacher = session.scalars(select(Teacher.id)).all()
    for _ in range(0, NUMBER_SUBJECT):
        subject = Subject(sub_name=fake_data.unique.subject(), teacher_id=choice(ids_teacher))
        session.add(subject)
    session.commit()

    for _ in range(0, NUMBER_GROUP):
        group = Group(gr_name=fake_data.msisdn())
        session.add(group)
    session.commit()

    ids_group = session.scalars(select(Group.id)).all()
    for _ in range(0, NUMBER_STUDENTS):
        student = Student(full_name=fake_data.name(), group_id=choice(ids_group))
        session.add(student)
    session.commit()
        
    ids_student = session.scalars(select(Student.id)).all()
    ids_subject = session.scalars(select(Subject.id)).all()
    for _ in range(0, NUMBER_STUDENTS * 20):
        marks = Journal(mark=randint(1, 10), subject_id=choice(ids_subject), student_id=choice(ids_student))
        session.add(marks)
    session.commit()


    session.close()
