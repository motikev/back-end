#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, User, Course, Enrollment, CourseContent

fake = Faker()

# Create a context to use the app imported as a reference to populate the data
with app.app_context():
    # Create sample data for User model
    users = []
    for i in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash="hashed_password",  # You should hash the password
            profile_info=fake.sentence(20),  # Ensure profile info is at least 20 characters
        )
        db.session.add(user)
        users.append(user)

    db.session.commit()

    # Create sample data for Course model
    courses = []
    course_categories = ["IT Courses", "Design Courses"]
    for category in course_categories:
        for i in range(3):  # Three courses per category
            course = Course(
                title=fake.catch_phrase(),
                description=fake.sentence(50),
                category=category,
                instructor_id=fake.random_int(min=1, max=5),  # Random instructor assignment
                enrollment_limit=fake.random_int(min=10, max=50),  # Random enrollment limit
            )
            db.session.add(course)
            courses.append(course)

    db.session.commit()

    # Create sample data for Enrollment model
    enrollments = []
    for user in users:
        for course in courses:
            enrollment = Enrollment(
                user_id=user.user_id,
                course_id=course.course_id,
            )
            db.session.add(enrollment)
            enrollments.append(enrollment)

    db.session.commit()

    # Create sample data for CourseContent model
    course_contents = []
    topics = [
        "Introduction to Software Engineering",
        "Web Development Basics",
        "React Application Fundamentals",
        "UX/UI Design Principles",
        "Graphic Design Fundamentals",
    ]
    for course in courses:
        for topic in topics:
            content = CourseContent(
                course_id=course.course_id,
                topic=topic,
                content=fake.paragraphs(3),  # Simulated course content paragraphs
            )
            db.session.add(content)
            course_contents.append(content)

    # Add all CourseContent instances to the session and commit to the database
    db.session.commit()

# Print this statement if the data has been populated
print("Sample data has been populated.")
