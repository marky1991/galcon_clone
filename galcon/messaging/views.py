# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from braces.views import LoginRequiredMixin

from .models import Pm
from . import my_forms

from galcon.models import Player
from groups.models import Group

class Messages_Base_View(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        """Here we need to put all the desired attributes in the instance's
namespace before calling View's dispatch function. (It returns a response, so
all variables must be saved before calling it)"""
        self.prepare_dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    def prepare_dispatch(self, request, *args, **kwargs):
        """This function goes through the mro and calls each
parent class' setup function. Finally, it calls its own. (Combined with the reversed
call, we go from the top of the mro to the bottom.)"""
        for cls in reversed(type(self).__mro__):
            if hasattr(cls, "setup"):
                cls.setup(self, request, *args, **kwargs)

        self.setup(request, *args, **kwargs)
    def setup(self, request, *args, **kwargs):
        """This method is very similar to the traditional __init__
function. It can be assumed that superclass setup functions have already been
run. (So using variables defined in superclass' setup functions is fine)"""
        if hasattr(request.user, "player"):
            self.draft_count = request.user.player.written_messages.filter(sent=False).count()
        else:
            self.draft_count = 0
        self.url_root = "inbox"
        self.direction = "recieved"
        self.filter = None
    def get(self, request, *args, message_id=None, page_number=None, **kwargs):
        #inheritance doesn't make sense here.
        #super().get(request, *args, message_id=None, page_number=None, **kwargs)
        if message_id is None:
            if page_number is not None:
                if self.direction == "sent":
                    messages = request.user.player.written_messages
                    if self.filter:
                        messages = messages.filter(**self.filter)
                    else:
                        messages = messages.all()
                else:
                    messages = request.user.player.recieved_messages.all()
                    bad_messages = [related_object for related_object in messages if related_object.object is None]
                    #More hacks
                    request.user.player.recieved_messages.remove(*bad_messages)
                    #The if clause is a temporary hack.
                    messages = [related_object.object for related_object in messages if related_object.object]
                    if self.filter:
                        def query(msg):
                            for key, value in self.filter.items():
                                if getattr(msg, key) != value:
                                    return False
                            return True
                        messages = list(filter(query, messages))
                    
                pages = Paginator(messages, 20)
                groups = pages.page(page_number)
            else:
                return HttpResponseRedirect("/messages/" + self.url_root + "/1/")
            template = "messaging/messages.html"
        else:
            try:
                messages = request.user.player.recieved_messages.all().generic_objects()
                message = list(filter(lambda msg: msg.slug==message_id, messages))[0]
            except ObjectDoesNotExist:
                raise Http404()
            group_recipients = []
            user_recipients = []
            for recipient in message.recipients.all():
                if hasattr(recipient, "members"):
                    group_recipients.append(recipient)
                else:
                    user_recipients.append(recipient)
            author_name = message.author.user.username
            recipient_names = []
            for recipient in list(map(lambda obj: obj.object, message.recipients.all())):
                if hasattr(recipient, "name"):
                    recipient_names.append(recipient.name)
                else:
                    recipient_names.append(recipient.user.username)
    

                                            
            template = "messaging/message.html"

        Locals = dict(locals())
        Locals.update(self.__dict__)
        return render(request, template, Locals)
    def post(self, request, *args, message_id=None, **kwargs):
        action = request.POST.get("action", "")

        if message_id is None:
            ids = request.POST.getlist("target_messages")
        else:
            ids = [message_id]
        for msg_id in ids:
            try:
                message = Pm.objects.get(slug=msg_id)
            except ObjectDoesNotExist:
                raise Http404
            if action == "trash":
                message.deleted = True
            elif action == "mark_read":
                message.read = True
            elif action == "mark_unread":
                message.read = False
            elif action == "star":
                message.starred = True
            elif action == "unstar":
                message.starred = False
            else:
                return None
            message.save()
        print("Redirecting to", request.path)
        return HttpResponseRedirect(request.path)
        
        
        
    
class Inbox(Messages_Base_View):
    def setup(self, request, *args, message_id=None, **kwargs):
        self.filter = {"deleted": False}
    def post(self, request, *args, message_id=None, page_number=None, **kwargs):

        action = request.POST["action"]
        if message_id is None:
            ids = request.POST.getlist("target_messages")
        else:
            ids = [message_id]
        for msg_id in ids:
            try:
                message = Pm.objects.get(slug=msg_id)
            except ObjectDoesNotExist:
                raise Http404
            if action == "trash":
                message.deleted = True
                message.save()
            elif action == "mark_read":
                message.read = True
                message.save()
            elif action == "mark_unread":
                message.read = False
                message.save()
            elif action == "star":
                message.starred = True
                message.save()
            elif action == "unstar":
                message.starred = False
                message.save()
            elif action == "reply" or action == "reply_all" or action == "forward":
                try:
                    reply_message = Pm.objects.get(slug=message_id)
                    recipient_names = []
                    for recipient in list(map(lambda obj: obj.object, reply_message.recipients.all())):
                        if hasattr(recipient, "name"):
                            recipient_names.append(recipient.name)
                        else:
                            recipient_names.append(recipient.user.username)
                except ObjectDoesNotExist:
                    return Http404()

                if action == "reply":
                    user_recipients = [reply_message.author.user.username]
                    group_recipients = []
                elif action == "reply_all":
                    recipients = list(map(lambda recipient: recipient.object, reply_message.recipients.all()))
                    users = filter(lambda recipient: hasattr(recipient, "user"),recipients)
                    groups = filter(lambda recipient: not hasattr(recipient, "user"), recipients)
                    user_recipients = list(set([
                        reply_message.author.user.username] + list(
                            map(lambda x: x.user.username, users))))

                    group_recipients = list(map(lambda group: group.name, groups))
                    print(user_recipients, group_recipients, "recipiens")
                elif action == "forward":
                    recipients = list(map(lambda recipient: recipient.object, reply_message.recipients.all()))
                    user_recipients = []
                    group_recipients = []
                    

                if not reply_message.title.startswith("Re: ") and "reply" in action:
                    title = "Re: " + reply_message.title
                elif not reply_message.title.startswith("Fwd: ") and "forward" == action:
                    title = "Fwd: " + reply_message.title
                else:
                    title = reply_message.title

                if "forward" == action:
                    text = """---------- Forwarded message ----------
From: {}
Date: {}
Subject: {}
To: {}""".format(reply_message.author.user.username, str(reply_message.post_date),
                 reply_message.title, ", ".join(recipient_names))
                else:
                    text = ""

                    
                    
                    
                pm = Pm.create(title=title, text=text)
                self.form = my_forms.Modify_Message_Form(instance=pm)
                Locals = dict(locals())
                Locals.update(self.__dict__)
                
                return render(request, "messaging/new_message.html",
                              Locals)
                """if message.title.startswith("Re: "):
                    title = message.title
                else:
                    title = "Re: " + message.title
                new_message = Pm(author=request.user.player,
                                                title=title)
                new_message.save()
                new_message.recipients.connect(message.author)
                message.next=new_message
                message.save()"""

        return HttpResponseRedirect("/messages/inbox/")
        

class Message(Messages_Base_View):
    def setup(self, request, *args, message_id=None, **kwargs):
        message = get_object_or_404(Pm, slug=message_id)
        
        if message.sent:
            self.cls = Inbox
        else:
            self.cls = Modify_Message
            
    def get(self, request, *args, message_id=None, **kwargs):
        return self.cls.get(self, request, *args, message_id=message_id, **kwargs)

    def post(self, request, *args, message_id=None, **kwargs):
        return self.cls.post(self, request, *args, message_id=message_id, **kwargs)

class Starred_Messages(Messages_Base_View):
    def setup(self, request, *args, url=None, **kwargs):
        self.url_root = "starred"
        self.filter = {"starred": True}

class Sent_Messages(Messages_Base_View):
    def setup(self, request, *args, url=None, **kwargs):
        self.url_root = "sent"
        self.direction = "sent"
        self.filter = {"sent": True}

class Drafts(Messages_Base_View):
    def setup(self, request, *args, url=None, **kwargs):
        self.url_root = "drafts"
        self.direction = "sent"
        self.filter = {"sent": False}

class Trash(Messages_Base_View):
    def setup(self, request, *args, url=None, **kwargs):
        self.url_root = "trash"
        self.filter = {"deleted": True}

class Modify_Message(Messages_Base_View):
    url_root = "new"
    def get(self, request, message_id=None):
        if message_id is not None:
            message = get_object_or_404(Pm, slug=message_id)
            self.form = my_forms.Modify_Message_Form(instance=message)
        else:
            self.form = my_forms.Modify_Message_Form()
        Locals = dict(locals())
        Locals.update(self.__dict__)
        return render(request, "messaging/new_message.html", Locals)

    def post(self, request, message_id=None):
        data = request.POST.copy()
        action = request.POST.get("action", "")
        recipients = []
        author = request.user.player

        for group_name in map(str.strip, data["recipient_groups"].split(",")):
            if group_name:
                recipients.append(Group.objects.get(name=group_name))

        for username in map(str.strip, data["recipient_users"].split(",")):
            if username:
                recipients.append(Player.objects.get(user__username=username))
            
        data["author"] = author.pk
        data["recipients"] = map(lambda thing: thing.pk, recipients)


        if message_id is not None:
            message = get_object_or_404(Pm, slug=message_id)
            self.form = my_forms.Modify_Message_Form(data=data, instance=message)
        else:
            self.form = my_forms.Modify_Message_Form(data=data)
        if action == "send" or action == "save_draft":
            if self.form.is_valid():
                self.form.instance.sent = action == "send"
                self.form.instance.author = author
                self.form.instance.post_date = timezone.now()
                self.form.instance._recipients = recipients
                self.form.save()
                return HttpResponseRedirect("/messages/inbox/")
            else:

                return HttpResponseRedirect("/messages/inbox/")
        elif action == "discard":
            print(dir(message), "DIR")
            return HttpResponseRedirect("/messages/inbox/")
        
