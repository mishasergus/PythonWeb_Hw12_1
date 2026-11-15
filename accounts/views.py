from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect


# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("booking:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})