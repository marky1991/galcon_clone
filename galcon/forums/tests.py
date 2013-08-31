from unittest import expectedFailure

from django.contrib.auth.models import User

from galcon.tests import My_Test_Case as TestCase
from .models import Post, Thread, Subsection, Section
from .templatetags import forums_util as util

from galcon import settings

latest_post_info = util.latest_post_info


class Test_Forums(TestCase):
    fixtures = ["users.json", "forum.json"]
    def test_template(self):
        response = self.client.get("/forums/")
        self.assertTemplateUsed("base.html")
        
    def test_thread(self):
        settings.child_per_page = 2
        response = self.client.get("/forums/development/dev/1/")

class Test_Create_Thread(TestCase):
    fixtures = ["users.json", "forum.json"]
    def setUp(self):
        super().setUp() 
        self.client.post("/login/", {"username": "example_user",
                                     "password": "password"})
        
    def test_template(self):
        print("\n\n\nStarting test template\n\n\n")
        response = self.client.get("/forums/development/dev/new_thread/")
        self.assertTemplateUsed("modify_post.html")
        
    def test_thread_created(self):
        """Only checks to see if the thread object was created.
Doesn't check that it's got a post."""
        old_count = Thread.objects.filter(parent__slug="dev", parent__parent__slug="development").count()
        response = self.client.get("/forums/development/dev/")
        p = Subsection.objects.all()
        parent = Subsection.objects.filter(slug="dev", parent__slug="development")[0]
        self.client.post("/forums/development/dev/new_thread/",
                                    {"title" : "This Is a Test",
                                     "text" : "This is only a test."})
        new_count = Thread.objects.filter(parent__slug="dev", parent__parent__slug="development").count()
        self.assertEqual(new_count, old_count + 1)
        
    def test_has_post(self):
        self.client.post("/forums/development/dev/new_thread/",
                         {"title" : "This Is a Test",
                          "text" : "This is only a test."})
        new_thread = Thread.objects.filter(parent__slug="dev",
                                        parent__parent__slug="development").latest()
        self.assertTrue(new_thread.children.all().count() > 0)
        
    def test_post_has_data(self):
        self.client.post("/forums/development/dev/new_thread/",
                         {"title" : "This Is a Test",
                          "text" : "This is only a test."})
        new_thread = Thread.objects.filter(parent__slug="dev",
                                        parent__parent__slug="development").latest()
        children = list(new_thread.children.all())
        self.assertEqual(children[0].title, "This Is a Test")
        self.assertEqual(children[0].text, "This is only a test.")
        try:
            int(children[0].slug)
        except ValueError:
            self.fail("Noninteger slug for post: {}".format(children[0].slug))

class Test_Edit_Post(TestCase):
    fixtures = ["users.json", "forum.json"]
    def setUp(self):
        super().setUp()
        self.post = Post.objects.get(pk=7)
        self.old_title = self.post.title
        self.old_text = self.post.text
        self.old_author = self.post.author
        self.old_modification_date = self.post.last_modification_date
        self.client.post("/login/", {"username": "example_user",
                             "password": "password"})
        
    def test_template(self):
        response = self.client.get("/forums/development/dev/2/7/edit/")
        self.assertTemplateUsed("modify_post.html")
        
    def test_edit_title(self):
        self.client.post("/forums/development/dev/2/7/edit/",
                         {"title" : "New Title",
                          "text" : self.old_text})
        new_post = Post.objects.get(pk=7)
        self.assertEqual(new_post.title, "New Title")
        self.assertEqual(self.old_text, new_post.text)
        self.assertEqual(self.old_author, new_post.author)
        self.assertTrue(self.old_modification_date < new_post.last_modification_date)
        
    def test_edit_text(self):
        self.client.post("/forums/development/dev/2/7/edit/",
                         {"title" : self.old_title,
                          "text" : "New text."})
        new_post = Post.objects.get(pk=7)
        self.assertEqual(new_post.title, self.old_title)
        self.assertEqual("New text.", new_post.text)
        self.assertEqual(self.old_author, new_post.author)
        self.assertTrue(self.old_modification_date < new_post.last_modification_date)
        
    def test_edit_nothing(self):
        self.client.post("/forums/development/dev/2/7/edit/",
                         {"title" : self.old_title,
                          "text" : self.old_text})
        new_post = Post.objects.get(pk=7)
        self.assertEqual(new_post.title, self.old_title)
        self.assertEqual(self.old_text, new_post.text)
        self.assertEqual(self.old_author, new_post.author)
        self.assertEqual(self.old_modification_date, new_post.last_modification_date)

class Test_Reply(TestCase):
    fixtures = ["users.json", "forum.json"]
    def setUp(self):
        super().setUp()
        self.thread = Thread.objects.get(pk=2)
        self.client.post("/login/", {"username": "example_user",
                             "password": "password"})
        self.user = User.objects.get(username="example_user")
        
    def test_template(self):
        response = self.client.get("/forums/development/dev/2/7/reply/")
        self.assertTemplateUsed("modify_post.html")
        
    def test_reply(self):
        old_post_count = self.thread.children.all().count()
        response = self.client.post("/forums/development/dev/2/7/reply/",
                                    {"title": "Re: Lies",
                                     "text": "Your a doo-doo head."})
        post = self.thread.children.all().latest()
        new_post_count = self.thread.children.all().count()
        self.assertEqual(new_post_count, old_post_count + 1)
        post = self.thread.children.all().latest()
        self.assertEqual(post.text, "Your a doo-doo head.")
        self.assertEqual(post.title, "Re: Lies")
        self.assertEqual(post.author.user, self.user)
        


#================================
#Template tags
#================================
class Test_Latest_Post_Info(TestCase):
    fixtures = ["forum.json", "users.json"]
    def setUp(self):
        super().setUp()
        thread = Thread.objects.get(slug="2")
        other_thread = Thread.objects.get(slug="3")
        self.thread_context = {"child":  thread, "request": self.Fake_Request()}
        self.other_thread_context = {"child":  other_thread, "request": self.Fake_Request()}
        
        section = Section.objects.get(slug="development")
        self.section_context = {"child": section, "request": self.Fake_Request()}

        subsection = Subsection.objects.get(slug="more_stuff")
        self.subsection_context = {"child": subsection, "request": self.Fake_Request()}
        
    def test_thread(self):
        latest_post = latest_post_info(self.thread_context, "thread")
        self.assertHTMLEqual(latest_post, "<a href='/forums/other/more_stuff/2/7/'>" + \
            "Thread #2</a><br/>example_user<br/>Jul 12, 2013 @ 3:07 p.m.")
        
    def test_other_thread(self):
        #Tests that the latest post from a thread truly belongs to it
        latest_post = latest_post_info(self.other_thread_context, "thread")
        self.assertHTMLEqual(latest_post, "<a href='/forums/other/more_stuff/3/8/'>" + \
            "Thread #3</a><br/>example_user<br/>Jul 11, 2013 @ 3:07 p.m.")
        
    def test_section(self):
        latest_post = latest_post_info(self.section_context, "section")
        self.assertHTMLEqual(latest_post, "<a href='/forums/development/dev/1/5/'>" + \
            "Beep Boop</a><br/>example_user<br/>Jul 8, 2013 @ 3:07 p.m.")
        
    def test_subsection(self):
        latest_post = latest_post_info(self.subsection_context, "subsection")
        self.assertHTMLEqual(latest_post, "<a href='/forums/other/more_stuff/2/7/'>" + \
            "Thread #2</a><br/>example_user<br/>Jul 12, 2013 @ 3:07 p.m.")

class Test_Small_Templatetags(TestCase):
    """This test tests all the dinky templatetags that are barely worth testing"""
    fixtures = ["users.json", "forum.json"]
    def setUp(self):
        self.thread = Thread.objects.get(pk=2)
        super().setUp()
        class Fake_Field:
            def __init__(self, errors):
                self.errors = errors
        self.context = {"child": self.thread, "request": self.Fake_Request()}
        self.field = Fake_Field(["bad url", "bad name"])
        
    def test_me(self):
        txt = util.me(self.context)
        self.assertEqual(txt, "example_user")
        
    def test_make_url(self):
        txt = util.make_url("bob's supercool water-world$!$!$!$")
        self.assertEqual(txt, "bob's_supercool_water-world")
        
    def test_plaintext(self):
        txt = util.plaintext("<b><big><h3><span>Hi</span></h3></big></b>")
        self.assertEqual(txt, "Hi")

    @expectedFailure
    def test_child_link(self):
        txt = util.child_link(self.context)
        self.assertEqual(txt, '<a href="/forums/other/more_stuff/2/">Thread #2</a>')
        
    def test_format_date(self):
        txt = util.format_date(self.thread.post_date)
        self.assertEqual(txt,self.thread.post_date.date())
        self.client.post("/login/", {"username": "example_user",
                             "password": "password"})
        txt = util.format_date(self.thread.post_date)
        self.assertEqual(txt, self.thread.post_date.date())
        
    def test_format_time(self):
        txt = util.format_time(self.thread.children.all()[0].last_modification_date)
        self.assertEqual(txt, "Jul 9, 2013 @ 7:07 p.m.")

    def test_render_post(self):
        self.client.post("/login/", {"username": "example_user",
                             "password": "password"})
        util.render_post(self.context, "<span>/me says hello</span>")
        self.assertEqual(self.context["post"], "<span>example_user says hello</span>")
        
    def test_lookup(self):
        out = util.lookup({"a": "b"}, "a")
        self.assertEqual(out, "b")
        
    def test_get_attr(self):
        class Cow:
            def __init__(self, name):
                self.name = name
        bessie = Cow("Bessie")
        out = util.get_attr(bessie, "name")
        self.assertEqual(out, "Bessie")

    def test_to_flag(self):
        out = util.to_flag(-1)
        self.assertHTMLEqual(out, "<img src='/site/flags/0.gif'/>")
        out = util.to_flag(5)
        self.assertHTMLEqual(out, "<img src='/site/flags/5.gif'/>")

    def test_render_errors(self):
        out = util.render_errors(self.field)
        self.assertHTMLEqual(out, "<div class='error'>bad url</div>/n<div class='error'>bad name</div>")
        
