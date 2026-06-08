from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "환영합니다! 첫 메모를 작성해보세요.")
            return redirect("memo:list")
    else:
        form = UserCreationForm()

    return render(request, "users/signup.html", {"form": form})