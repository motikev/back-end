#!/usr/bin/env python3
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Course, Enrollment, CourseContent
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
CORS(app)
# home
# routes
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first():
            return make_response(jsonify({'message': 'Username already exists'}), 400)
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}), 201)


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            db.session['user_id'] = user.id
            return make_response(jsonify({'message': 'Login successful'}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid credentials'}), 401)


class CheckSession(Resource):
    def get(self):
        if 'user_id' in db.session:
            user = User.query.get(db.session['user_id'])
            if user:
                return make_response(jsonify({'username': user.username}), 200)
        return make_response(jsonify({'message': 'Not logged in'}), 401)


class Logout(Resource):
    def post(self):
        db.session.pop('user_id', None)
        return make_response(jsonify({'message': 'Logged out successfully'}), 200)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.as_dict())
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.password = data['password']
            user.email = data['email']
            user.profile_info = data.get('profile_info')
            db.session.commit()
            return jsonify(user.as_dict())
        return {'message': 'User not found'}, 404
    
    def patch(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            db.session.commit()
            return jsonify(user.as_dict())
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.as_dict() for user in users])

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        profile_info = data.get('profile_info')
        user = User(username=username, password=password, email=email, profile_info=profile_info)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.as_dict()), 201



class CourseResource(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        if course:
            return jsonify(course.as_dict())
        return {'message': 'Course not found'}, 404

    def put(self, course_id):
        course = Course.query.get(course_id)
        if course:
            data = request.get_json()
            course.title = data['title']
            course.description = data['description']
            course.category = data['category']
            course.instructor_id = data['instructor_id']
            course.enrollment_limit = data['enrollment_limit']
            db.session.commit()
            return jsonify(course.as_dict())
        return {'message': 'Course not found'}, 404

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return {'message': 'Course deleted'}
        return {'message': 'Course not found'}, 404


class CourseListResource(Resource):
    def get(self):
        courses = Course.query.all()
        return jsonify([course.as_dict() for course in courses])

    def post(self):
        data = request.get_json()
        title = data['title']
        description = data['description']
        category = data['category']
        instructor_id = data['instructor_id']
        enrollment_limit = data.get('enrollment_limit')
        course = Course(title=title, description=description, category=category, instructor_id=instructor_id, enrollment_limit=enrollment_limit)
        db.session.add(course)
        db.session.commit()
        return jsonify(course.as_dict()), 201


class EnrollmentResource(Resource):
    def get(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            return jsonify(enrollment.as_dict())
        return {'message': 'Enrollment not found'}, 404

    def put(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            data = request.get_json()
            enrollment.user_id = data['user_id']
            enrollment.course_id = data['course_id']
            db.session.commit()
            return jsonify(enrollment.as_dict())
        return {'message': 'Enrollment not found'}, 404

    def delete(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            return {'message': 'Enrollment deleted'}
        return {'message': 'Enrollment not found'}, 404


class EnrollmentListResource(Resource):
    def get(self):
        enrollments = Enrollment.query.all()
        return jsonify([enrollment.as_dict() for enrollment in enrollments])

    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        course_id = data['course_id']
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify(enrollment.as_dict()), 201


class CourseContentResource(Resource):
    def get(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            return jsonify(content.as_dict())
        return {'message': 'CourseContent not found'}, 404
    def put(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            data = request.get_json()
            content.course_id = data['course_id']
            content.topic = data['topic']
            content.content = data['content']
            db.session.commit()
            return jsonify(content.as_dict())
        return {'message': 'CourseContent not found'}, 404

    def delete(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            db.session.delete(content)
            db.session.commit()
            return {'message': 'CourseContent deleted'}
        return {'message': 'CourseContent not found'}, 404


class CourseContentListResource(Resource):
    def get(self):
        contents = CourseContent.query.all()
        return jsonify([content.as_dict() for content in contents])

    def post(self):
        data = request.get_json()
        course_id = data['course_id']
        topic = data['topic']
        content_text = data['content']
        content = CourseContent(course_id=course_id, topic=topic, content=content_text)
        db.session.add(content)
        db.session.commit()
        return jsonify(content.as_dict()), 201



api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(CourseResource, '/courses/<int:course_id>')
api.add_resource(CourseListResource, '/courses')
api.add_resource(EnrollmentResource, '/enrollments/<int:enrollment_id>')
api.add_resource(EnrollmentListResource, '/enrollments')
api.add_resource(CourseContentResource, '/contents/<int:content_id>')
api.add_resource(CourseContentListResource, '/contents')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5555)