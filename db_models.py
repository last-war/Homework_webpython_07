from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from connector import Base


class Group(Base):
    __tablename__ = 'study_groups'
    id = Column(Integer, primary_key=True)
    gr_name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey('study_groups.id', ondelete='CASCADE'))
    group = relationship('Group', back_populates='students')


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    sub_name = Column(String(50), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', back_populates='subjects')


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    mark = Column(Integer)
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    subject = relationship('Subject', back_populates='journal')
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship('Student', back_populates='journal')
