from django.contrib import admin
from .models import Course, Enrollment, Post


# Define admin classes for your models
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_name", "professor", "created_at")


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")


class PostAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "created_at")


# Register your models with their respective admin classes
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Post, PostAdmin)
