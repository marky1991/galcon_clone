#Maps username to Chat_Player
#This dict maintains persistance of users.
users = {}
max_line_length = 100

__all__ = ["views", "models", "templates"]

from django.utils import timezone

import collections
from gevent import queue
"""
class Room:
    def __init__(self):
        self.server = Server_Player()
        self.users = set([self.server])
        self.lines = collections.deque(maxlen=50)

    def login(self, user):
        self.users.add(user)
        self.print("{0} has joined.".format(user.username))
        
    def logout(self, user):
        self.users.remove(user)
        self.print("{0} has left.".format(user.username))

    def backlog(self, size=50):
        return list(self.lines)[-size:]

    def post(self, line):
        self.broadcast(line)
        self.lines.append(line)

    def broadcast(self, line):
        for user in self.users:
            user.put(line)
    def print(self, *args, author=None, sep=" "):
        if author is None:
            author = self.server
        text = sep.join(args)
        line = models.Line(author_name=author.username, post_date=timezone.now(), text=text)
        self.lines.append(line)
        self.broadcast(line)

class Chat_Player:
    def __init__(self, username, is_admin):
        self.username = username
        self.is_admin = is_admin
        self.queue = queue.Queue()
    def put(self, line):
        self.queue.put_nowait(line)

class Server_Player(Chat_Player):
    def __init__(self):
        super().__init__("Server", True)
    def put(self, line):
        super().put(line)
        line.save()"""


from . import views, models
