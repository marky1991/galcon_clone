from django.db import models
from . import max_line_length
from django.contrib.auth.models import User
from django.utils import timezone
from django.template import defaultfilters as filters

from galcon import settings

class Chat_User(models.Model):
    user = models.OneToOneField(User, related_name="chat_user")
    room = models.ForeignKey("Room", related_name="users", null=True, blank=True)
    #Represents the id of the last message seen
    last_seen_id = models.PositiveIntegerField(default=0, editable=False)

    def login(self, room_name="main"):
        self.room = Room.objects.get(name=room_name)
        print("Room: ", self.room)
        
        lines = self.room.lines.all().reverse()
        line_count = lines.count()
        if line_count < settings.chat_history_size:
            index = line_count - 1
        else:
            index = settings.chat_history_size - 1
        self.last_seen_id = lines[index].id
        self.save()
        self.room.users.add(self)
        self.room.print("{0} has joined.".format(self.user.username))
        
    def logout(self):
        self.room.print("{0} has left.".format(self.user.username))
        print(self.room, "printed")
        self.room.users.remove(self)
        
    def post(self, text):
        line = Line(author=self, post_date=timezone.now(),
                    text=text, room=self.room)
        line.save()
        self.last_seen_id = line.id
        #We bump up the id because we include the post client-side
        #instead of waiting to send->recieve->show to avoid lag
        self.save()
    
class Line(models.Model):
    """Represents a line of chat."""
    class Meta:
        get_latest_by = "post_date"
        ordering = ["post_date"]
    author = models.ForeignKey(Chat_User)
    post_date = models.DateTimeField()
    text = models.TextField(max_length=max_line_length)
    room = models.ForeignKey("Room", related_name="lines")
    
    def toJSON(self):
        return {"author_name": str(self.author.user.username),
                "post_date": filters.date(self.post_date, "P"),
                "text": str(self.text)}
    def __str__(self):
        return self.text

class Room(models.Model):
    """Represents a chat room. (Duh)"""

    name = models.TextField(max_length=50)
    admins = models.ManyToManyField(Chat_User, related_name="admined_chat_rooms", blank=True, null=True)

    def backlog(self, starting_id=None):
        if starting_id is None:
            raise TypeError("Starting id must not be None.")
        return list(self.lines.filter(pk__gt=starting_id).all())

    def print(self, *args, sep=" "):
        chat_user = Chat_User.objects.get(user__username="server")
        chat_user.room = self
        text = sep.join(args)
        chat_user.post(text)
        
