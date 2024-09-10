from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


from users.models import *
from users.forms import *

@require_http_methods(["GET", "POST"])
def register(request):
    
    template = "users/registration.html"
    
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Félicitations ! Vous êtes inscris sur la plateforme, connectez-vous pour commencer à trouver de nouvelles collabs !",
            )
            return redirect("home")
        else:
            messages.info(
                request, "Veuillez remplir le formulaire de manière adéquate."
            )
    else:
        form = CustomUserCreationForm()

    return render(request, template, {"form": form})
