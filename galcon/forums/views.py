# Create your views here.

from collections import OrderedDict
from braces.views import LoginRequiredMixin

from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.utils import timezone
from django.views.decorators.cache import never_cache, cache_control
from django.utils.decorators import method_decorator

from .models import Section, Subsection, Thread, Post
from .util import clean_post, Forum_Spot
from . import my_forms

from galcon.models import section_to_rank
from galcon import settings

class Forum_Base_View(View):
    def dispatch(self, request, *args, url=None, **kwargs):
        """Here we need to put all the desired attributes in the instance's
namespace before calling View's dispatch function. (It returns a response, so
all variables must be saved before calling it)"""
        self.prepare_dispatch(request, *args, url=url, **kwargs)
        return super().dispatch(request, *args, url=url, **kwargs)
    def prepare_dispatch(self, request, *args, url=None, **kwargs):
        """This function goes through the mro and calls each
parent class' setup function. Finally, it calls its own. (Combined with the reversed
call, we go from the top of the mro to the bottom.)"""
        for cls in reversed(type(self).__mro__):
            if hasattr(cls, "setup"):
                cls.setup(self, request, *args, url=url, **kwargs)

        self.setup(request, *args, url=url, **kwargs)
    def setup(self, request, *args, url=None, **kwargs):
        """This method is very similar to the traditional __init__
function. It can be assumed that superclass setup functions have already been
run. (So using variables defined in superclass' setup functions is fine)"""
        if url is None:
            url = "forums/"
        else:
            url = "forums/" + url
        self.spot = Forum_Spot(url)
        if self.spot.level != "post":
            self.template = "forums/" + self.spot.level + ".html"
        else:
            self.template = "forums/thread.html"
        self.url = url

    @property
    def breadcrumbs(self):
        breadcrumbs = OrderedDict()
        current_url = "/"
        #if self.url is not None:
        #    for crumb in self.url.strip("/").split("/"):
                #current_url = current_url + crumb + "/"
                #breadcrumbs[crumb.title()] = current_url
        for level, slug in self.spot:
            if level != "forum":
                crumb = globals()[level.title()].objects.get(slug=slug).title
            else:
                crumb = "Forums"
            current_url = current_url + slug + "/"
            breadcrumbs[crumb.title()] = current_url
        print(breadcrumbs, "CRB")
        return breadcrumbs

class Forums(Forum_Base_View):
    @method_decorator(cache_control(must_revalidate=True, no_cache=True, no_store=True))
    def get(self, request, *args, **kwargs):
        post_count = 0
        rank = section_to_rank.get(self.spot.section, "")

        #The way I'm doing this is odd. I ought to just piece together the
        #parent object and access parent.children directly.
        if self.spot.level == "forum":
            children = Section.objects.all()
            headers = ["Forum", "Topics", "Last Post"]
        elif self.spot.level == "section":
            children = Subsection.objects.filter(parent__slug=self.spot.section)
            post_count = Post.objects.filter(parent__parent__parent__slug=self.spot.section).count()
            headers = ["Topic", "Threads", "Posts", "Last Post"]
        elif self.spot.level == "subsection":
            children = Thread.objects.filter(parent__slug=self.spot.subsection,
                                             parent__parent__slug=self.spot.section
                                             ).annotate(latest_edit=
                                                        models.Max("children__last_modification_date")
                                                        ).order_by("-latest_edit")
            post_count = Post.objects.filter(parent__parent__slug=self.spot.subsection).count()
            print("viewing sub")
            headers = ["Thread", "Author", "Replies", "Views", "Last Post"]
        elif self.spot.level == "thread" or self.spot.level == "post":
            children = Post.objects.filter(parent__id__exact=int(self.spot.thread))
            #Because I don't allow empty threads, this cannot raise an error.
            parent= children[0].parent
            parent.page_views = parent.page_views + 1
            parent.save()
            template = "forums/thread.html"
            headers = []
        
        children = Paginator(children, 20).page(1)
        return render(request, self.template, {"request": request,
                                                "children": children,
                                                "level": self.spot.level,
                                                "headers": headers,
                                               "rank": rank,
                                                "post_count": post_count,
                                                  "breadcrumbs": list(self.breadcrumbs.items())})

class Recent_Posts(Forum_Base_View):
    @method_decorator(cache_control(must_revalidate=True, no_cache=True, no_store=True))
    def get(self, request, *args, **kwargs):
        print("HI")
        self.spot.subsection = None
        self.template = "forums/recent_posts.html"
        headers = ["Subsection", "Thread", "Replies", "Last Post"]
        children = Thread.objects.filter(parent__parent__slug=self.spot.section,
                                             ).annotate(latest_edit=
                                                        models.Max("children__last_modification_date")
                                                        ).order_by("-latest_edit")[:settings.recent_post_limit]
        
        return render(request, self.template, {"request": request,
                                        "children": children,
                                        "level": self.spot.level,
                                        "headers": headers,
                                          "breadcrumbs": list(self.breadcrumbs.items())})


class Modify_Post(LoginRequiredMixin, Forum_Base_View):
    def setup(self, request, *args, url=None, action=None, **kwargs):
        if action is None:
            raise Http404
        self.thread_id, self.post_id = self.url.strip("/").split("/")[-2:]

        self.action = action

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(slug=self.post_id)
        if self.action == "reply":
            form = my_forms.Modify_Post_Form()
        else:
            form = my_forms.Modify_Post_Form(instance=post)
        return render(request, "forums/modify_post.html",
                      {"request": request,
                       "form": form,
                       "action": self.action,
                       "post": post,
                       "breadcrumbs": list(self.breadcrumbs.items())})
    def post(self, request, *args, **kwargs):
        original_url = "/".join(self.url.strip("/").split("/")[:-1])
        if self.action == "edit":
            try:
                post_id = int(self.post_id)
            except ValueError:
                raise Http404
            instance = get_object_or_404(Post, id=post_id)
            old_title, old_text = instance.title, instance.text
            instance.text = clean_post(instance.text)
            form = my_forms.Edit_Post_Form(data=request.POST, instance=instance)
            if form.is_valid():
                if form.instance.title != old_title or form.instance.text != old_text:
                    form.instance.last_modification_date = timezone.now()
                    form.save()
                if not original_url.endswith("/"):	
                    original_url = original_url + "/"
                return HttpResponseRedirect("/" + original_url)
        elif self.action == "reply":
            form = my_forms.Create_Post_Form(data=request.POST)
            if form.is_valid():
                post = Post.create(title=form.data["title"], text=form.data["text"], author=request.user.player,
                            parent_id=self.thread_id, post_date=None)
                post.save()
                return HttpResponseRedirect("/" + original_url + "/")
            else:
                raise NotImplemented("Need to tell you why it was invalid")
        else:
            raise Http404
        return render(request, "forums/modify_post.html",
                      {"request": request,
                       "form": form,
                       "action": self.action,
                       "post": reply_post,
                       "breadcrumbs": list(self.breadcrumbs.items())})

class Create_Thread(LoginRequiredMixin, Forum_Base_View):
    def get(self, request, url=None):
        form = my_forms.Create_Thread_Form()
        return render(request, "forums/modify_post.html", {"request": request,
                                                  "form": form,
                                                "action": "create_thread",
                                                "breadcrumbs": list(self.breadcrumbs.items())})
    def post(self, request, *args, **kwargs):
        form = my_forms.Create_Thread_Form(data=request.POST)
        if form.is_valid():
            now = timezone.now()
            parent = Subsection.objects.get(slug=self.spot.subsection, parent__slug=self.spot.section)
            author = request.user.player
            thread = Thread.create(author=author,
                            post_date=now,
                            parent=parent,
                        post=Post.prepare(title=form.data["title"],
                            author=author,
                            post_date=now,
                            text=form.data["text"],))
            thread.save()
            return HttpResponseRedirect("/" + self.url)
        else:
            raise NotImplemented("Need to warn about errors")
        return render(request, "forums/modify_post.html", {"request": request,
                                                  "form": form,
                                                "action": "create_thread",
                                                "breadcrumbs": list(self.breadcrumbs.items())})
