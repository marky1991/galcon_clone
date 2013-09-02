from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from django.utils.unittest import expectedFailure


from .settings import PROJECT_PATH
import galcon

from .templatetags.galcon_util import format_time

import os
from bs4 import BeautifulSoup as soupify


class My_Client(Client):
    """Just follows redirects by default"""
    def get(self, *args, **kwargs):
        if "follow" not in kwargs:
            kwargs["follow"] = True
        return super().get(*args, **kwargs)
    def post(self, *args, **kwargs):
        if "follow" not in kwargs:
            kwargs["follow"] = True
        return super().post(*args, **kwargs)

Old_Test = TestCase
class My_Test_Case(Old_Test):
    def setUp(self):
        #This function gets the request from the context.
        #So far, all it uses is the session and the child.
        #If anything else is accessed, the test needs to be updated
        class Fake_Request:
            @property
            #I'm using a non-"self" self to avoid overwriting the outer
            #self
            def session(request_self):
                return self.client.session
            @property
            def path(request_self):
                return self.client
        self.Fake_Request = Fake_Request
        super().setUp()
    client_class = My_Client

#Monkeypatching used without regret
TestCase = My_Test_Case

class Home_Test(TestCase):
    def test_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed("base.html")

class Games_Test(TestCase):
    def test_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed("games.html")        

class Login_Test(TestCase):
    fixtures = ["users.json"]
    def test_template(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed("login.html")
        
    def test_opening_screen(self):
        response = self.client.get("/login/")
        soup = soupify(response.content.decode("utf8"))
        self.assertTrue(soup.find("form", id="login_form"))
        
    def test_success(self):
        response = self.client.post("/login/", {"username": "example_user",
                                                "password": "password"})
        self.assertRedirects(response, "/")
        self.assertTrue('_auth_user_id' in self.client.session)
        
    def test_wrong_password(self):
        response = self.client.post("/login/", {"username": "example_user",
                                                "password": "wrong_password"})
        self.assertTemplateUsed("login.html")
        self.assertTrue(len(response.context["form"].errors) == 1)
        self.assertFormError(response, "form", None, "Please enter a " + \
"correct username and password. Note that both fields may be case-sensitive.")
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_unknown_account(self):
        response = self.client.post("/login/", {"username": "unknown_user",
                                                "password": "idk"})
        self.assertTemplateUsed("login.html")
        self.assertFormError(response, "form", None, "Please enter a " + \
"correct username and password. Note that both fields may be case-sensitive.")
        self.assertTrue(len(response.context["form"].errors) == 1)
        self.assertFalse('_auth_user_id' in self.client.session)
        
class Logout_Test(TestCase):
    fixtures = ["users.json"]
    def setUp(self):
        self.client.post("/login/", {"username": "example_user",
                                     "password": "password"})
        
    def test_success(self):
        def find_login_button(tag):
            children = list(tag.children)
            for child in children:
                if hasattr(child, "attrs") and "href" in child.attrs:
                    if child["href"] == "/login/":
                        return True
            return False
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/")
        soup = soupify(response.content)
        self.assertTrue(soup.find_all(find_login_button, class_="top_button"))
        self.assertFalse('_auth_user_id' in self.client.session)

class Test_Register(TestCase):
    def test_opening_screen(self):
        response = self.client.get("/register/")
        self.assertTrue("checked_age" in response.context)
        self.assertFalse(response.context["checked_age"])

    def test_too_young(self):
        response = self.client.post("/register/", {"old_enough": False})
        self.assertTemplateUsed("too_young_for_registration.html")
        
    def test_old_enough(self):
        response = self.client.post("/register/", {"old_enough": True})
        self.assertTemplateUsed("register.html")
        soup = soupify(response.content)
        self.assertTrue(soup.find("form", id="register_form"))

    @expectedFailure
    def test_bad_data(self):
        self.assertTrue(False)

class Test_Profile(TestCase):
    fixtures = ["users.json"]
    def test_known_player(self):
        response = self.client.get("/users/example_user/")
        self.assertFalse("<h1>Player doesn't exist!</h1>" in
                         response.content.decode("utf8"))
    def test_unknown_player(self):
        response = self.client.get("/users/unknown_user/")
        self.assertEqual(response.status_code, 404)
    def test_successful_find_friend(self):
        response = self.client.post("/users/example_user/",
                                    {"friend_name": "example_user"})
        self.assertRedirects(response, "/users/example_user/")
    def test_blank_find_friend(self):
        response = self.client.post("/users/example_user/",
                                    {"friend_name": ""})
        self.assertRedirects(response, "/users/example_user/")
        
    @expectedFailure
    def test_close_find_friend(self):
        response = self.client.post("/users/",
                                    {"friend_name": "example_us"})
        self.assertTemplateUsed("profile_matches.html")
        self.assertRedirects(response, "/users/example_user/")
    def test_unsuccessful_find_friend(self):
        response = self.client.post("/users/example_user/",
                                    {"friend_name": "moo"})
        self.assertEqual(response.status_code, 404)

class Test_Friends(TestCase):
    fixtures = ["users.json"]
    def test_template(self):
        response = self.client.get("/users/example_user/friends/")
        self.assertTemplateUsed("friends.html")
    def test_no_friends(self):
        response = self.client.get("/users/friendless_user/friends/")
        self.assertTrue("friendless_user has no friends. :(" in
                        response.content.decode("utf8"))
    def test_success(self):
        response = self.client.get("/users/example_user/friends/")
        soup = soupify(response.content)
        self.assertEqual(soup.find("example_user has no friends. :("), None)
        self.assertTemplateUsed("friends.html")
    def test_unknown_user(self):
        response = self.client.get("/users/unknown_user/friends/")
        self.assertEqual(response.status_code, 404)

class Test_Edit_Profile(TestCase):
    fixtures = ["users.json"]
    def setUp(self):
        self.client.post("/login/", {"username": "example_user",
                                     "password": "password"})
    def test_template(self):
        response = self.client.get("/users/example_user/edit/")
        self.assertTemplateUsed("edit_profile.html")
    def test_get_other(self):
        response = self.client.get("/users/friendless_user/edit/")
        self.assertRedirects(response, "/users/friendless_user/")
    def test_edit_success(self):
        avatar = open(os.path.join(PROJECT_PATH, "fixtures", "avatar.jpg"), "rb")
        response = self.client.post("/users/example_user/edit/",
                                    {"password1": "new_password",
                                     "password2": "new_password",
                                     "location": "Cooltown",
                                     "avatar": avatar,
                                     "email": "example_user@gmail.com",
                                     "registration_code": "Teehee",
                                     "get_newsletter": "False"})
        self.assertFalse(len(response.context["form"].errors))
        user = User.objects.get(username="example_user")
        player = user.player
        
        self.assertTrue(check_password("new_password", user.password))
        self.assertTrue(player.location == "Cooltown")
        self.assertTrue(player.avatar != None)
        self.assertTrue(user.email == "example_user@gmail.com")
        self.assertTrue(player.registration_code == "Teehee")
        self.assertFalse(player.get_newsletter)
        avatar.close()
        
    @expectedFailure
    def test_bad_data(self):
        self.assertTrue(False)

    def tearDown(self):
        self.client.get("/logout/")

class Test_Modify_Newsletter(TestCase):
    def test_template(self):
        response = self.client.get(
            "/users/friendless_user/edit/newsletter_prefs/")
        self.assertTemplateUsed("modify_newsletter_prefs.html")
    @expectedFailure
    def test_set(self):
        response = self.client.post("/users/friendless_user/edit/newsletter_prefs/",
                                    {"subscribe": "True"})
        player = User.objects.get(username="friendless_user").player
        self.assertTrue(player.get_newsletter)
        response = self.client.post("/users/friendless_user/edit/newsletter_prefs/",
                                    {"subscribe": "False"})
        self.assertFalse(player.get_newsletter)
