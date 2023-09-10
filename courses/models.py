from django.db import models
from django.conf import settings


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="enrollments", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="enrollments", on_delete=models.CASCADE
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.course_name}"


class Post(models.Model):
    course = models.ForeignKey(Course, related_name="posts", on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post in {self.course.course_name}"
