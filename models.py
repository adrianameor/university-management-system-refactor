from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

# Login manager loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(10), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False) #Rafida - Step 4
    role = db.Column(db.String(10), nullable=False)

# Define models
class Classroom(db.Model):
    __tablename__ = 'classroom'
    building = db.Column(db.String(15), primary_key=True)
    room_number = db.Column(db.String(7), primary_key=True)
    capacity = db.Column(db.Integer)

class Department(db.Model):
    __tablename__ = 'department'
    dept_name = db.Column(db.String(20), primary_key=True)
    building = db.Column(db.String(15))
    budget = db.Column(db.Numeric(12,2))

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(8), primary_key=True)
    title = db.Column(db.String(50))
    dept_name = db.Column(db.String(20), db.ForeignKey('department.dept_name'))
    credits = db.Column(db.Integer)
    department = db.relationship('Department', backref=db.backref('courses', lazy=True))

class Instructor(db.Model):
    __tablename__ = 'instructor'
    ID = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept_name = db.Column(db.String(20), db.ForeignKey('department.dept_name'))
    salary = db.Column(db.Numeric(8,2))
    department = db.relationship('Department', backref=db.backref('instructors', lazy=True))

class Section(db.Model):
    __tablename__ = 'section'
    course_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(15))
    room_number = db.Column(db.String(7))
    time_slot_id = db.Column(db.String(4))
    course = db.relationship('Course', backref=db.backref('sections', lazy=True))
    classroom = db.relationship('Classroom', foreign_keys=[building, room_number], 
                                primaryjoin="and_(Section.building==Classroom.building, Section.room_number==Classroom.room_number)")

class Teaches(db.Model):
    __tablename__ = 'teaches'
    ID = db.Column(db.String(5), db.ForeignKey('instructor.ID'), primary_key=True)
    course_id = db.Column(db.String(8), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    instructor = db.relationship('Instructor', backref=db.backref('teaches', lazy=True))
    section = db.relationship('Section', foreign_keys=[course_id, sec_id, semester, year], 
                              primaryjoin="and_(Teaches.course_id==Section.course_id, Teaches.sec_id==Section.sec_id, Teaches.semester==Section.semester, Teaches.year==Section.year)")

class Student(db.Model):
    __tablename__ = 'student'
    ID = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept_name = db.Column(db.String(20), db.ForeignKey('department.dept_name'))
    tot_cred = db.Column(db.Integer)
    department = db.relationship('Department', backref=db.backref('students', lazy=True))

class Takes(db.Model):
    __tablename__ = 'takes'
    ID = db.Column(db.String(5), db.ForeignKey('student.ID'), primary_key=True)
    course_id = db.Column(db.String(8), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    semester = db.Column(db.String(6), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(2))
    student = db.relationship('Student', backref=db.backref('takes', lazy=True))
    section = db.relationship('Section', foreign_keys=[course_id, sec_id, semester, year], 
                              primaryjoin="and_(Takes.course_id==Section.course_id, Takes.sec_id==Section.sec_id, Takes.semester==Section.semester, Takes.year==Section.year)")

class Advisor(db.Model):
    __tablename__ = 'advisor'
    s_ID = db.Column(db.String(5), db.ForeignKey('student.ID'), primary_key=True)
    i_ID = db.Column(db.String(5), db.ForeignKey('instructor.ID'))
    student = db.relationship('Student', backref=db.backref('advisor', uselist=False))
    instructor = db.relationship('Instructor', backref=db.backref('advisees', lazy=True))

class Prereq(db.Model):
    __tablename__ = 'prereq'
    course_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), primary_key=True)
    prereq_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), primary_key=True)
    course = db.relationship('Course', foreign_keys=[course_id], 
                             primaryjoin="Prereq.course_id==Course.course_id", 
                             backref=db.backref('prereqs', lazy=True))
    prereq_course = db.relationship('Course', foreign_keys=[prereq_id], 
                                    primaryjoin="Prereq.prereq_id==Course.course_id", 
                                    backref=db.backref('required_by', lazy=True))

class Timeslot(db.Model):
    __tablename__ = 'timeslot'
    time_slot_id = db.Column(db.String(4), primary_key=True)
    day = db.Column(db.String(1), primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)