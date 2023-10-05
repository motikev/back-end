from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

# Initialize the database through SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    # Create the table columns
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the one-to-many relationship with courses (instructor)
    courses = db.relationship('Course', backref='instructor', lazy=True)

    # Define the many-to-many relationship with enrollments
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Course(db.Model):
    __tablename__ = 'courses'

    # Create the table columns
    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # Add category field
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    enrollment_limit = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the one-to-many relationship with enrollments
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

    # Define the one-to-many relationship with course content
    contents = db.relationship('CourseContent', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.title}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    # Create the table columns
    enrollment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Enrollment ({self.enrollment_id})>'


class CourseContent(db.Model):
    __tablename__ = 'course_contents'

    # Create the table columns
    content_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CourseContent ({self.content_id})>'
