from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from gevent import queue
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from . import models

import json

class SmartEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "toJSON"):
            return obj.toJSON()
        return super().default(obj)

@login_required
def join(request, room_slug=None):
    if room_slug is None:
        return HttpResponseRedirect("/chat/main/join/")
    try:
        username = request.user.username
    except TypeError:
        username = "Anonymous"
    user = request.user
    
    try:
        chat_user = user.chat_user
    except ObjectDoesNotExist:
        chat_user = models.Chat_User(last_seen_id=0,
                                     user=user)
        chat_user.save()
    chat_user.login(room_slug=room_slug)
    
    return HttpResponseRedirect("/chat/" + room_slug + "/")
@login_required
def main(request, room_slug=None):
    chat_user = request.user.chat_user
    if chat_user.room is None:
        return HttpResponseRedirect("/chat/" + room_slug + "/join/")

    return render(request, "chat/room.html", {"request": request,
                                              "room_name": chat_user.room.name,
                                         "username": request.user.username})

@login_required
def leave(request):
    chat_user = request.user.chat_user
    chat_user.logout()
    return HttpResponse("")

@login_required
def post(request):
    chat_user = request.user.chat_user

    message = request.POST["message"]
    chat_user.post(message)
    return HttpResponse("")

@login_required
def poll(request):
    chat_user = request.user.chat_user
    room = chat_user.room
    if room:
        messages = room.backlog(starting_id=chat_user.last_seen_id)
        if messages:
            chat_user.last_seen_id = messages[-1].id
            chat_user.save()
            return HttpResponse(json.dumps(messages, cls=SmartEncoder))
    return HttpResponse("")
    
