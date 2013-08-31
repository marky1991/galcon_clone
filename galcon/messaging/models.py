from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from galcon import settings
from galcon.models import Player
from galcon.util import cached_property

from genericm2m.models import RelatedObjectsDescriptor

# Create your models here.

class Pm(models.Model):
    """Represents a private message (a la email) from one user to another."""
    
    title = models.CharField(max_length=settings.max_title_length, default="(Blank)")
    slug = models.SlugField(max_length=settings.max_title_length, editable=False)
    #author = models.ForeignKey(Player, related_name="written_messages")
    #recipient = models.ForeignKey(Player, related_name="recieved_messages")
    next = models.OneToOneField("self", related_name="previous", null=True, blank=True)
    post_date = models.DateTimeField(editable=False)
    text = models.TextField(max_length=settings.max_post_length)
    read = models.BooleanField(default=False)
    sent= models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    author_content_type = models.ForeignKey(ContentType, related_name="pm_content_types")
    author_object_id = models.PositiveIntegerField()

    """recipient_content_type = models.ForeignKey(ContentType, related_name="b")
    recipient_object_id = models.PositiveIntegerField()
    recipient = generic.GenericForeignKey('recipient_content_type', 'recipient_object_id')"""

    #Both will be either a group or a player
    author = generic.GenericForeignKey('author_content_type', 'author_object_id')

    recipients = RelatedObjectsDescriptor()

    def to_url(self):
        return str(self.id)
    @cached_property
    def full_url(self):
        url_pieces = []
        target = child
        url_pieces.append(target.to_url())
        while hasattr(target, "parent"):
            target = target.parent
            url_pieces.append(target.to_url())
        return "/".join(reversed(url_pieces))

    @classmethod
    def create(cls, recipients=None, post_date=None, title="(Blank)",
               text="", **kwargs):
        if post_date is None:
            post_date = timezone.now()
        obj = cls(title=title, text=text,
                    post_date=post_date)
        if recipients is not None:
            obj._recipients = recipients
        else:
            obj._recipients = []
        return obj
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = self.to_url()
        if hasattr(self, "_recipients"):
            for recipient in self._recipients:
                self.recipients.connect(recipient)
                recipient.recieved_messages.connect(self)
                #In generic-m2m, connetions are one-way
                if hasattr(recipient, "members"):
                    recipient.recieved_messages.connect(self)
                    for member in recipient.members.all():
                        member.recieved_messages.connect(self)
                print("Connecting ", self, "to ", recipient)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}->{} - {}".format(self.author, list(map(lambda x: x.object, self.recipients.all())), self.title)


class Friend_Request(models.Model):
    author = models.ForeignKey(Player, related_name="sent_%(class)ss")
    recipient = models.ForeignKey(Player, related_name="%(class)ss")
    #None represents not-yet-answered
    #False transforms this into a block
    accepted = models.NullBooleanField(default=None)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return "".join(["{}(".format(type(self).__name__), self.author, "->", self.recipient, " ", "accepted=", self.accepted])
