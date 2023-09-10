# create_users_courses_posts.py
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from courses.models import (
    Course,
    Enrollment,
    Post,
)  # Replace 'your_app_name' with the name of your Django app containing these models

# Create 2 student users
student1 = CustomUser.objects.create_user(
    id="student1",
    name="Student One",
    student_id="s1",
    role="student",
    password="password123",
)
student2 = CustomUser.objects.create_user(
    id="student2",
    name="Student Two",
    student_id="s2",
    role="student",
    password="password123",
)

# Create 2 professor users
professor1 = CustomUser.objects.create_user(
    id="professor1",
    name="Professor One",
    student_id="p1",
    role="professor",
    password="password123",
)
professor2 = CustomUser.objects.create_user(
    id="professor2",
    name="Professor Two",
    student_id="p2",
    role="professor",
    password="password123",
)

# Each professor creates a course
course1 = Course.objects.create(
    course_name="Course One",
    description="Description for Course One",
    professor=professor1,
)
course2 = Course.objects.create(
    course_name="Course Two",
    description="Description for Course Two",
    professor=professor2,
)

# Each professor adds 2 posts to their course
Post.objects.create(
    course=course1,
    title="Post 1 in Course One",
    content="Content for Post 1 in Course One",
)
Post.objects.create(
    course=course1,
    title="Post 2 in Course One",
    content="Content for Post 2 in Course One",
)
Post.objects.create(
    course=course2,
    title="Post 1 in Course Two",
    content="Content for Post 1 in Course Two",
)
Post.objects.create(
    course=course2,
    title="Post 2 in Course Two",
    content="Content for Post 2 in Course Two",
)

# Each student enrolls in each course
Enrollment.objects.create(student=student1, course=course1)
Enrollment.objects.create(student=student1, course=course2)
Enrollment.objects.create(student=student2, course=course1)
Enrollment.objects.create(student=student2, course=course2)

print("Users, Courses, Enrollments and Posts have been created.")
