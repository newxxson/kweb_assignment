"""
URL configuration for kweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from courses import views as course_view
from accounts import views as accounts_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", course_view.redirect_to_home, name="redirect_to_home"),
    # courses
    path("create-course/", course_view.create_course, name="create_course"),
    path("list-courses/<str:show_all>/", course_view.list_courses, name="list_courses"),
    path(
        "show-create-post/<int:course_id>/",
        course_view.show_create_post,
        name="show_create_post",
    ),
    path("create-post/<int:course_id>/", course_view.create_post, name="create_post"),
    path("list-post/<int:course_id>/", course_view.list_post, name="list_post"),
    path("show-post/<int:post_id>/", course_view.show_post, name="show_post"),
    path("edit-post/<int:post_id>/", course_view.edit_post, name="edit_post"),
    path("delete-post/<int:post_id>/", course_view.delete_post, name="delete_post"),
    path(
        "kick-student/<int:course_id>/<str:student_id>/",
        course_view.kick_student,
        name="kick_student",
    ),
    path(
        "list-enrolled-students/<int:course_id>/",
        course_view.list_enrolled_students,
        name="list_enrolled_students",
    ),
    path("enroll/<int:course_id>/", course_view.enroll, name="enroll"),
    path("list-all-post/", course_view.list_all_post, name="list_all_post"),
    # accounts
    path("login/", accounts_view.user_login, name="login"),
    path("signup/", accounts_view.user_signup, name="signup"),
    path("logout/", accounts_view.user_logout, name="logout"),
]
