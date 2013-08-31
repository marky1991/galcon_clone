from collections import defaultdict

from django.db import models
from django.utils import timezone
from django.forms import ValidationError
from django.contrib.contenttypes import generic

from galcon.models import My_Model, Player
from galcon import settings
from galcon.templatetags import galcon_util as util

from genericm2m.models import RelatedObjectsDescriptor

class Group(My_Model):
    class Meta:
        get_latest_by = "creation_time"
    name = models.CharField(max_length=settings.max_name_length)
    slug = models.SlugField(max_length=settings.max_title_length, blank=True)
    creation_time = models.DateTimeField(default=timezone.now, blank=True)
    members = models.ManyToManyField(Player, through="groups.Membership", related_name="groups")
    description = models.TextField(max_length=settings.max_post_length)
    hidden = models.BooleanField(default=False)
    join_requires_approval = models.BooleanField(default=False)

    written_messages = generic.GenericRelation("messaging.Pm",
                                               content_type_field='author_content_type',
                               object_id_field='author_object_id')
    """recieved_messages = generic.GenericRelation("messaging.Pm",
                                                content_type_field='recipient_content_type',
                               object_id_field='recipient_object_id')"""
    recieved_messages = RelatedObjectsDescriptor()

    @property
    def owners(self):
        return self.members.filter(membership__adminship="owner")

    @property
    def superadmins(self):
        return (self.members.filter(membership__adminship="owner") |
            self.members.filter(membership__adminship="superadmin"))

    @property
    def admins(self):
        return (self.members.filter(membership__adminship="owner") |
            self.members.filter(membership__adminship="superadmin") |
            self.members.filter(membership__adminship="admin"))
    
    def to_url(self):
        return util.make_url(self.name)

    def __str__(self):
        return str(self.name)

    def __contains__(self, thing):
        return Membership.objects.filter(player=thing, group=self).exists()

    @classmethod
    def create(cls, name=None, creation_time=None,
               admin=None, description=None, hidden=False, join_requires_approval=None, **kwargs):
        if admin is None:
            raise ValueError("""You cannot create a group without any members.
In Group.save, pass a admin=admin keyword arg please.""")
        if creation_time is None:
            creation_time = timezone.now()
        obj = cls(name=name,
                  creation_time=creation_time,
                  description=description,
                  hidden=hidden,
                  join_requires_approval=join_requires_approval)
        obj._admin = admin
        return obj
    
    def clean(self, *args, **kwargs):
        if self.name in ["new", "smallest", "biggest", "oldest", "newest"]:
            raise ValidationError({"name": [ValidationError(
                """That name cannot be used. (It would make the urls ambiguous)""")]})
        super().clean(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        self.slug = self.to_url()

        super().save(*args, **kwargs)
        if hasattr(self, "_admin"):
            assert self._admin is not None
            membership = Membership.objects.create(player=self._admin,
                               group=self,
                               adminship="owner")
            membership.save()

class Membership(models.Model):
    class Meta:
        unique_together = (("player", "group"),)
    player = models.ForeignKey("galcon.Player")
    group = models.ForeignKey(Group)
    #Possible values: "admin", "owner", "superadmin", "none"
    adminship = models.TextField(max_length=50, blank=False, choices=settings.adminship_levels)

    def clean(self, *args, **kwargs):
        if list(self.group.owners.all()) == [self.player] and self.adminship != "owner": 
            raise ValidationError("""You cannot remove the last owner.
(Delete the group if you don't want it anymore.)""")
        super().clean(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if list(self.group.owners.all()) == [self.player]:
            raise ValidationError("""You cannot remove the last owner.
(Delete the group if you don't want it anymore.)""")
        else:
            print("Supreseriously deleting")
            super().delete(*args, **kwargs)

rank_to_num = {"none": 0, "admin": 1, "superadmin": 2, "owner": 3}

class Join_Group_Request(models.Model):
    class Meta:
        unique_together = (("author", "recipient"),)
    author = models.ForeignKey(Player, related_name="sent_%(class)ss")
    recipient = models.ForeignKey(Group, related_name="%(class)ss")
    #None represents not-yet-answered
    #False transforms this into a block
    accepted = models.NullBooleanField(default=None)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return "".join(["{}(".format(type(self).__name__), str(self.author), "->", str(self.recipient), " ", "accepted=", str(self.accepted), ")"])


