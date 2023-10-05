from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Course, Enrollment  # Import your models from models.py

app = Flask(__name__)

# Configure the database URI (adjust as needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elearning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the E-Learning Platform!'

# User routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'user_id': user.user_id, 'username': user.username} for user in users]
    return jsonify(user_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'profile_info': user.profile_info
        })
    return jsonify({'message': 'User not found'}), 404

# Course routes
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    course_list = [{'course_id': course.course_id, 'title': course.title} for course in courses]
    return jsonify(course_list)

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course:
        return jsonify({
            'course_id': course.course_id,
            'title': course.title,
            'description': course.description,
            'instructor_id': course.instructor_id
        })
    return jsonify({'message': 'Course not found'}), 404

# Enrollment routes
@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    enrollment_list = [{'enrollment_id': enrollment.enrollment_id, 'user_id': enrollment.user_id, 'course_id': enrollment.course_id} for enrollment in enrollments]
    return jsonify(enrollment_list)

@app.route('/enrollments/<int:enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if enrollment:
        return jsonify({
            'enrollment_id': enrollment.enrollment_id,
            'user_id': enrollment.user_id,
            'course_id': enrollment.course_id
        })
    return jsonify({'message': 'Enrollment not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
