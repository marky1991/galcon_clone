import os

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.utils.decorators import classonlymethod
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.db import models
from django.forms.models import model_to_dict

from django.contrib.auth import forms, authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import galcon
from . import my_forms
from .models import Player, section_to_rank
from .settings import STATIC_URL

def home(request):
    """This view renders the home page. The home page shows nothing but static html for now."""
    return render(request, "base.html", {"request": request})

def games(request):
    """This view renders the games page. The games page shows nothing but static html for now."""
    return render(request, "galcon/games.html")

def igalcon(request):
    return render(request, "galcon/igalcon.html")

def fusion(request):
    return render(request, "galcon/fusion.html")

def support(request):
    return render(request, "galcon/support.html")

def login(request):
    redirect_url = "/"
    if request.GET and "next" in request.GET:
            redirect_url = request.GET["next"]
    if request.method == "GET":
        form = forms.AuthenticationForm()
    else:
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                if user.is_active:
                    log_in(request, user)
                    return HttpResponseRedirect(redirect_url)
                else:
                    #TODO: Show errors
                    assert False, data
            assert False, data
    return render(request, "galcon/login.html", {"request": request,
                                          "form": form})
def logout(request):
    log_out(request)
    return HttpResponseRedirect("/")

def register(request):
    form = None
    if request.method == "GET":
        return render(request, "galcon/register.html", {"request": request,
                                                 "checked_age": False})
    else:
        if "old_enough" in request.POST:
            old_enough = request.POST["old_enough"] == "True"
            if old_enough:
                form = my_forms.Create_Player_Form()
        else:
            form = my_forms.Create_Player_Form(data=request.POST)
            old_enough=True
            if form.is_valid():
                user = User.objects.create_user(form.data["username"],
                                                form.data["email"],
                                                form.data["password1"])
                user.save()
                logged_in_user = authenticate(username=form.data["username"], password=form.data["password1"])
                log_in(request, logged_in_user)
                return HttpResponseRedirect("/")
            else:
                moo = dir(form)
                err = form.errors
                assert False
    return render(request, "galcon/register.html", {"request": request,
                                                     "form": form,
                                                     "checked_age": True,
                                                     "old_enough": old_enough})
def profile(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        player_exists = True
        player = user.player
        friends = player.friends.all()
        rank = ""
        trophies = player.trophies.all()
        return render(request, "galcon/profile.html", locals())
    #The post method is used for the "Find a friend box"
    else:
        if "friend_name" in request.POST and request.POST["friend_name"]:
            return HttpResponseRedirect("/users/" + request.POST["friend_name"] + "/")
        else:
            return HttpResponseRedirect("/users/" + username + "/")

def friends(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        player_exists = True
        player = user.player
        friends = player.friends.all()
        return render(request, "galcon/friends.html", locals())
    
@login_required
def edit_profile(request, username):
    """This view is responsible for showing the page used to edit a player's profile."""
    if request.user.username == username:
        if request.method == "GET":
            player = get_object_or_404(Player, user__username=username)
            data = model_to_dict(player)
            user_data = {"email": player.user.email,
                         "username": username}
            data.update(user_data)
            file_data = {"avatar": data["avatar"]}
            form = my_forms.Edit_Profile_Form(data, file_data)
        else:
            player = get_object_or_404(Player, user__username=username)
            data = request.POST.dict()
            data.update({"username": username})
            form = my_forms.Edit_Profile_Form(data, request.FILES)
            print(form.data, "DATA")
            if form.is_valid():
                if form.data["password1"] == form.data["password2"] and form.data["password1"] != "":
                    player.user.set_password(form.data["password1"])
                #The email is a required field, so no validation is needed
                player.user.email = form.data["email"]
                player.location = form.data.get("location", "")
                player.get_newsletter = form.data["get_newsletter"] == "True"
                if "avatar" in request.FILES:
                    player.avatar = request.FILES.get("avatar", "")
                player.registration_email = form.data.get("registration_email", "")
                player.registration_code= form.data.get("registration_code", "")
                player.user.save()
                player.save()
            
        return render(request, "galcon/edit_profile.html", {"request": request,
                                                     "form": form})
    else:
        return HttpResponseRedirect("/users/" + username + "/")


def highest_flag(request, username):
    player = Player.objects.get(user__username=username)
    max_value = 0
    for attribute in filter(lambda att_name:
                            att_name.endswith("_rank"), dir(player.rank)):
        val = getattr(player.rank, attribute)
        if val > max_value:
            max_value = val
    return HttpResponseRedirect(STATIC_URL + "flags" + "/" + str(max_value) + ".gif")
