from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment, Course, Post
from django.contrib.auth import get_user_model


# Create your views here.
# create courses
@login_required
def redirect_to_home(request):
    return redirect("/list-courses/show-all/")


# 교수 => 실제 코스 만들기, 만든 후 전체 코스 창으로 이동
@login_required
def create_course(request):
    if request.user.role != "professor":
        return show_error(request, error_message="You are not a professor")

    if request.method == "POST":
        course_name = request.POST.get("course_name")
        description = request.POST.get("description")
        if course_name:
            if not Course.objects.filter(course_name=course_name).exists():
                new_course = Course.objects.create(
                    course_name=course_name,
                    description=description,
                    professor=request.user,
                )
                return redirect("/list-courses/only/")
            else:
                return show_error(request, error_message=f"Course already exists")

    return render(request, "create_course.html")


# 교수 자기 코스 보기 or 전체, or 학생 전체 코스 보기
@login_required
def list_courses(request, show_all):
    user = request.user
    context = dict()
    if user.role == "professor":
        if show_all == "show-all":
            course = Course.objects.all()
        else:
            course = Course.objects.filter(professor=user)
    else:
        if show_all == "show-all":
            course = Course.objects.all()
        else:
            course = Course.objects.filter(enrollments__student=user)
        enrollments = Enrollment.objects.filter(student=user)
        enrolled_courses = [enrollment.course for enrollment in enrollments]
        context["enrolled_courses"] = enrolled_courses

    context["courses"] = course

    return render(request, "list_courses.html", context)


# 포스트 만드는 페이지 보여주기
@login_required
def show_create_post(request, course_id):
    user = request.user
    if user.role != "professor":
        return show_error(request, error_message="You are not a professor")

    course = Course.objects.filter(id=course_id)
    if not course.exists():
        return show_error(request, error_message="Course not found")
    course = course.first()
    if user == course.professor:
        return render(
            request,
            "show_create_post.html",
            {"course": course},
        )
    else:
        return show_error(request, error_message="Course not found")


# 포스트 만들기
@login_required
def create_post(request, course_id):
    user = request.user
    if user.role != "professor":
        return show_error(request, error_message="You are not a professor")

    if request.method == "POST":
        course = Course.objects.filter(id=course_id)
        if course.exists():
            course = course.first()
            if course.professor == user:
                title = request.POST.get("title")
                content = request.POST.get("content")
                course = course
                Post.objects.create(course=course, title=title, content=content)
                return redirect(f"/list-post/{course_id}/")
            else:
                return show_error(
                    request,
                    error_message="You are not the professor of this course",
                )
        else:
            return show_error(request, error_message="Course not found")

    return redirect(f"/show-create-post/{course_id}/")


# 강의 포스트 보여주기
@login_required
def list_post(request, course_id):
    user = request.user
    course = Course.objects.filter(id=course_id)
    if not course.exists():
        return show_error(request, error_message="Course not found")
    course = course.first()
    if course.professor == user or user.enrollments.filter(course=course).exists():
        posts = Post.objects.filter(course=course)
        return render(request, "list_post.html", {"posts": posts, "course": course})
    else:
        return show_error(request, error_message="You don't belong to this course")


# 특정 포스트 보여주기
@login_required
def show_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post.exists():
        post = post.first()
        return render(request, "show_post.html", {"post": post})
    else:
        return show_error(request, error_message="Post not found")


@login_required
def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id, course__professor=request.user)
    if not post.exists():
        return show_error(request, error_message="Post does not exist or UnAuthorized")
    if request.method == "POST":
        post = post.first()
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect(f"/list-post/{post.course.id}/")
    post = post.first()
    return render(request, "edit_post.html", {"post": post})


@login_required
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id, course__professor=request.user)
    if post.exists():
        post = post.first()
        course_id = post.course.id
        post.delete()
        return redirect(f"/list-post/{course_id}/")
    else:
        return show_error(request, error_message="Post does not exist or UnAuthorized")


# 강의 수강생 보여주기
@login_required
def list_enrolled_students(request, course_id):
    professor = request.user
    User = get_user_model()
    course = Course.objects.filter(id=course_id)
    if course.exists():
        course = course.first()
        if professor != course.professor:
            return show_error(
                request,
                error_message="You are not the professor of this course",
            )
        enrollment = Enrollment.objects.filter(course=course)
        students = [entry.student for entry in enrollment]
        return render(
            request,
            "list_enrolled_students.html",
            {"course": course, "students": students},
        )
    else:
        return show_error(request, error_message="Course not found")


# 강의 수강생 삭제하기
@login_required
def kick_student(request, course_id, student_id):
    user = request.user
    if user.role != "professor":
        return show_error(request, error_message="You are not a professor")

    course = Course.objects.filter(id=course_id)
    if course.exists() and course.first().professor == user:
        course = course.first()
        stduent_enrollment = Enrollment.objects.filter(
            student__student_id=student_id, course=course
        )
        if stduent_enrollment.exists():
            stduent_enrollment.delete()
            return redirect(f"/list-enrolled-students/{course_id}/")
        else:
            return show_error(request, error_message="no student id match")
    else:
        return show_error(request, error_message="Unauthorized access of no course")


# 수강 신청하기
@login_required
def enroll(request, course_id):
    user = request.user
    if user.role != "student":
        return show_error(request, error_message="You are not a student")
    course = Course.objects.filter(id=course_id)
    if not course.exists():
        return show_error(request, error_message="Course not found")

    course = course.first()
    enrollment = Enrollment.objects.create(student=user, course=course)

    return redirect("/list-courses/only/")


@login_required
def list_all_post(request):
    user = request.user
    if user.role != "student":
        return show_error(request, error_message="You are not a student")
    # Assuming student_id is known
    enrolled_courses = Course.objects.filter(enrollments__student=user)
    posts = Post.objects.filter(course__in=enrolled_courses).order_by("-created_at")

    return render(request, "list_all_post.html", {"posts": posts})


def show_error(request, error_message):
    return render(request, "error.html", {"error_message": error_message})
