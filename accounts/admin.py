from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    username_field = "id"
    list_display = ("id", "name", "student_id", "role", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "role")
    fieldsets = (
        (None, {"fields": ("id", "password")}),
        ("Personal Info", {"fields": ("name", "student_id", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("id", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )
    search_fields = ("id", "name", "student_id")
    ordering = ("id",)


# Register your custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
