from django.db import models
from django.utils import timezone

from galcon.models import My_Model, Player
from .templatetags import forums_util as util
from galcon.util import cached_property

from galcon import settings

class Note(models.Model):
    text = models.TextField(max_length=settings.max_title_length)

class Forum_Node(My_Model):
    class Meta:
        abstract = True
    slug = models.SlugField(max_length=settings.max_title_length, editable=False)

class Upper_Forum_Node(Forum_Node):
    class Meta:
        abstract = True
    title = models.CharField(max_length=settings.max_title_length, default="")
    description = models.CharField(max_length=settings.max_description_length)
    hidden = models.BooleanField(default=False)

class Section(Upper_Forum_Node):
    def to_url(self):
        return util.make_url(self.title)
    
    @cached_property
    def full_url(self):
        url_pieces = []
        target = child
        url_pieces.append(target.to_url())
        while hasattr(target, "parent"):
            target = target.parent
            url_pieces.append(target.to_url())
        return "/".join(reversed(url_pieces))
    
    """def clean(self, *args, **kwargs):
        if Section.objects.filter(slug=self.to_url()).exists():
            raise ValidationError("A section with a similar name already exists. Try again.")
        super().clean(*args, **kwargs)"""

    def __str__(self):
        return util.plaintext(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = self.to_url()
        super().save(*args, **kwargs)

#Could have used inheritance.
#Decided not to so all data is in one table. (Only one field is
#shared anyway) Removed here because lots of forum data is expected
class Subsection(Upper_Forum_Node):
    parent = models.ForeignKey(Section, related_name="children")
    
    def __str__(self):
        return util.plaintext(self.title)
    def to_url(self):
        return util.make_url(self.title)
    @cached_property
    def full_url(self):
        url_pieces = []
        target = child
        url_pieces.append(target.to_url())
        while hasattr(target, "parent"):
            target = target.parent
            url_pieces.append(target.to_url())
        return "/".join(reversed(url_pieces))
    def clean_self(self, *args, **kwargs):
        if Subsection.objects.filter(slug=self.to_url(), parent__id=self.parent.id).exists():
            raise ValidationError("A group with a similar name already exists. Try again.")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = self.to_url()
        super().save(*args, **kwargs)
class Thread(models.Model):
    class Meta:
        get_latest_by = "post_date"

    slug = models.SlugField(max_length=settings.max_title_length, editable=False)
    author = models.ForeignKey(Player, related_name="threads")
    post_date = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(Subsection, related_name="children")
    close_note = models.ForeignKey("Note", null=True, blank=True)
    sticky = models.BooleanField(default=False)
    page_views = models.IntegerField(default=0, editable=False)
    hidden = models.BooleanField(default=False)

    @classmethod
    def create(cls, author=None, post_date=None,
               parent=None, post=None, **kwargs):
        if post is None:
            raise ValueError("""You cannot create a thread without any posts.
In Thread.save, pass a post=post keyword arg please.""")
        if post_date is None:
            post_date = timezone.now()
        obj = cls(author=author, parent=parent,
                    post_date=post_date, close_note=None,
                   sticky=False)
        obj._post = post
        return obj
        
    def __str__(self):
        return util.plaintext(self.title)
    def to_url(self):
        return str(self.id)
    @property
    def title(self):
        try:
            return self.children.order_by("post_date")[0].title
        except IndexError:
            return ""
    @cached_property
    def full_url(self):
        url_pieces = []
        target = child
        url_pieces.append(target.to_url())
        while hasattr(target, "parent"):
            target = target.parent
            url_pieces.append(target.to_url())
        return "/".join(reversed(url_pieces))
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = self.to_url()
        super().save(*args, **kwargs)
        if hasattr(self, "_post"):
            assert self._post is not None
            self.children.add(self._post(self))

class PostManager(models.Manager):
    def latest(self, parent_id):
        return super().filter(parent__id__exact=parent_id).latest()
    def count(self, parent_id):
        return super().filter(parent__id__exact=parent_id).count()
    
class Post(Forum_Node):
    class Meta:
        get_latest_by = "last_modification_date"
        ordering = ["post_date"]
    title = models.TextField(max_length=settings.max_title_length)
    author = models.ForeignKey(Player, related_name="posts")
    parent = models.ForeignKey(Thread, related_name="children")
    post_date = models.DateTimeField(default=timezone.now)
    last_modification_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=settings.max_post_length)
    flag_note = models.ForeignKey("Note", blank=True, null=True)
    objects = PostManager()
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return util.plaintext(self.text)
    def to_url(self):
        return str(self.id)
    @classmethod
    def create(cls, title=None, text=None, author=None,
               parent_id=None, post_date=None):
        parent = Thread.objects.get(id=parent_id)
        if post_date is None:
            post_date = timezone.now()
        return cls(title=title, author=author, parent=parent,
                    post_date=post_date, text=text, last_modification_date=post_date,
                   flag_note=None)
    @staticmethod
    def prepare(**kwargs):
        """This function is admittedly wierd. (I think it's my first
real usage of closures in python)

Signature: Post.prepare(kwargs) -> curried_func(thread) -> Post
"""
        def create_post(thread):
            return Post.create(parent_id=thread.id, **kwargs)
        return create_post
    @cached_property
    def full_url(self):
        url_pieces = []
        target = self
        url_pieces.append(target.to_url())
        while hasattr(target, "parent"):
            target = target.parent
            url_pieces.append(target.to_url())
        return "/".join(reversed(url_pieces))
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = self.to_url()
        super().save(*args, **kwargs)
