from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def user_login(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["id"]
        password = request.POST["password"]
        user = authenticate(request, id=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "student":
                return redirect("/list-all-post/")
            else:
                return redirect("/list-courses/no/")
        else:
            error_message = "Incorrect ID or password"

    return render(request, "login.html", {"error_message": error_message})


def user_signup(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("id")
            password = form.cleaned_data.get("password1")
            user = authenticate(id=username, password=password)
            login(request, user)
            if user.role == "student":
                return redirect("/list-all-post/")
            else:
                return redirect("/list-courses/")

    return render(request, "signup.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")
