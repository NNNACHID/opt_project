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


@require_http_methods(["GET", "POST"])
def login_user(request):

    template = "users/login.html"
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, "Connexion ok !")
            return redirect("home")
        else:
            messages.info(request, "Données de connexion incorrectes")
    form = CustomAuthenticationForm()
    return render(request, template, {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")


def get_profile(request, pk):

    template = "users/profile.html"
    profile = get_object_or_404(CustomUserProfile, user=pk)
    context = {"profile": profile}
    return render(request, template, context)



def get_profile_list_by_type(request):

    url_name = resolve(request.path_info).url_name
    template = "users/users_list.html"

    if url_name == "creators":
        context = {
            "profiles": CustomUserProfile.objects.filter(user__role="creator")
        }
        return render(request, template, context)
    elif url_name == "advertisers":
        context = {
            "profiles": CustomUserProfile.objects.filter(user__role="advertiser")
        }
        return render(request, template, context)
    else:
        context = {
            "profiles": CustomUserProfile.objects.filter(user__role="association")
        }
        return render(request, template, context)
