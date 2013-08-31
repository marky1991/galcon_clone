from django.db import models
from . import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from .util import cached_property
from .templatetags import galcon_util as util

from django.forms import ValidationError

from genericm2m.models import RelatedObjectsDescriptor

section_to_rank = {"galcon_fusion": "fusion_rank",
                   "igalcon": "iphone_rank",
                   "flash": "flash_rank",
                   "classic_galcon": "classic_rank"}

"""For now, all the models are just shoved into one file.
Will seperate eventually."""

def save_file(filename, new_filename, folder):
    extension = filename.split(".")[-1]
    return folder + "/" + new_filename + "." + extension

class My_Model(models.Model):
    class Meta:
        abstract = True
    def clean(self, *args, **kwargs):
        try:
            other = type(self).objects.get(slug=self.to_url())
        except type(self).DoesNotExist:
            other = False
        if other and other.pk != self.pk:
            raise ValidationError(["A {} with a similar name already exists. Try again.".format(str(type(self)).lower().replace("_", " "))])
        super().clean(*args, **kwargs)
    def to_url(self):
        return str(self)


class Rank(models.Model):
    iphone_rank = models.IntegerField(default=0, editable=False)
    classic_rank = models.IntegerField(default=0, editable=False)
    flash_rank = models.IntegerField(default=0, editable=False)
    fusion_rank = models.IntegerField(default=0, editable=False)
    @staticmethod
    def make_default():
        rank = Rank()
        return rank
    
    def __str__(self):
        try:
            username = self.player.user.username
        except Player.DoesNotExist:
            username = "Unowned"
        return username+ "(" + ", ".join(map(str, [self.iphone_rank, self.classic_rank, self.flash_rank, self.fusion_rank])) + ")"

def save_trophy(instance, filename):
    return save_file(filename, ".".join(filename.split(".")[:-1]), "trophies")

class Trophy(models.Model):
    image = models.ImageField(upload_to=save_trophy)
    text = models.TextField(max_length=settings.max_title_length)
    def __str__(self):
        return str(self.text)

def save_avatar(instance, filename):
    return save_file(filename, instance.user.username, "avatars")

class Player(My_Model):
    #name ia covered by the django.auth User object
    user = models.OneToOneField(User)
    slug = models.SlugField(max_length=settings.max_title_length, default="", editable=False)
    friends = models.ManyToManyField("self", symmetrical=True,
                                     blank=True)
    post_count = models.PositiveIntegerField(default=0, editable=False)

    location = models.CharField(max_length=settings.max_location_length, blank=True)
    get_newsletter = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=save_avatar, blank=True)
    rank = models.OneToOneField("Rank", editable=False)
    hidden = models.BooleanField(default=False)
    registration_email = models.EmailField(blank=True)
    registration_code = models.CharField(max_length=settings.max_registration_code_length, blank=True)
    trophies = models.ManyToManyField("Trophy", blank=True, related_name="players")
    language = models.CharField(max_length=10, choices=settings.languages)

    written_messages = generic.GenericRelation("messaging.Pm",
                                               content_type_field='author_content_type',
                               object_id_field='author_object_id')
    """recieved_messages = generic.GenericRelation("messaging.Pm",
                                                content_type_field='recipient_content_type',
                               object_id_field='recipient_object_id')"""
    recieved_messages = RelatedObjectsDescriptor()

    def __str__(self):
        return self.user.username
    def to_url(self):
        return util.make_url(self.user.username)
    """def clean(self, *args, **kwargs):
        if Player.objects.filter(slug=self.to_url()).exists():
            raise ValidationError("A player with a similar name already exists. Try again.")
        super().clean(*args, **kwargs)"""
    def save(self, *args, **kwargs):
        try:
            existing_player = Player.objects.get(user=self.user)
            self.id = existing_player.id
        except Player.DoesNotExist:
            pass
        self.slug = self.to_url()
        rank = Rank.make_default()
        rank.save()
        self.rank = rank
        models.Model.save(self, *args, **kwargs)
