import random
import requests
from flask import request, jsonify, make_response
from faker import Faker
from app import app, db, User, Course, Enrollment, CourseContent

fake = Faker()

UNSPLASH_API_KEY = "1tzv_QUdaWTWvrIT-r6OgzTGHI1RxRxm6OVuaPvWjZA" 

# Function to create fake users
def create_fake_users(num_users):
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        profile_info = fake.paragraph()
        user = User(username=username, password=password, email=email, profile_info=profile_info)
        users.append(user)
    return users

def get_technology_image_url():
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_API_KEY}"
    }

    # Search for technology-related images using the Unsplash API
    response = requests.get("https://api.unsplash.com/photos/random", headers=headers, params={"query": "technology"})
    
    if response.status_code == 200:
        data = response.json()
        if "urls" in data:
            return data["urls"]["regular"]
    
    return None

# Function to create fake courses with technology-related images
def create_fake_courses(num_courses, instructors):
    courses = []
    for _ in range(num_courses):
        title = fake.catch_phrase()
        description = fake.text()
        category = fake.word()
        instructor = random.choice(instructors)
        enrollment_limit = random.randint(1, 100)
        image = get_technology_image_url()
        
        course = Course(
            title=title,
            description=description,
            category=category,
            instructor=instructor,
            enrollment_limit=enrollment_limit,
            image=image 
        )
        courses.append(course)
    return courses

# Function to create fake enrollments
def create_fake_enrollments(users, courses):
    enrollments = []
    for user in users:
        course = random.choice(courses)
        enrollment = Enrollment(user=user, course=course)
        enrollments.append(enrollment)
    return enrollments

# Function to create fake course content
def create_fake_course_contents(courses, min_word_count=700):
    contents = []
    for course in courses:
        topic = fake.sentence()
        content = ""

        while len(content.split()) < min_word_count:
            paragraph = fake.paragraph()
            content += paragraph + "\n"

        content_entry = CourseContent(course=course, topic=topic, content=content)
        contents.append(content_entry)
    return contents

if __name__ == "__main__":
    # Initialize the Flask app context
    with app.app_context():
        # Create and commit fake data
        num_fake_users = 10
        num_fake_courses = 20

        fake_users = create_fake_users(num_fake_users)
        fake_courses = create_fake_courses(num_fake_courses, fake_users)

        db.session.add_all(fake_users)
        db.session.add_all(fake_courses)
        db.session.commit()

        fake_enrollments = create_fake_enrollments(fake_users, fake_courses)
        db.session.add_all(fake_enrollments)

        # Generate and add fake course content
        fake_contents = create_fake_course_contents(fake_courses)
        db.session.add_all(fake_contents)

        db.session.commit()

    print("Fake data has been populated.")
