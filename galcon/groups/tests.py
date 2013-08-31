from bs4 import BeautifulSoup as soupify

from galcon.tests import My_Test_Case
from .models import Group
from galcon.models import Player

class Test_Group(My_Test_Case):
    fixtures = ["users.json", "groups.json"]
    def setUp(self):
        self.client.post("/login/", {"username": "example_user",
                                        "password": "password"})
    def test_template(self):
        response = self.client.get("/groups")
        self.assertTemplateUsed("groups.html")
        
    def test_redirect(self):
        
        response = self.client.get("/groups/")
        self.assertRedirects(response, "/groups/newest/1/")
        
        response = self.client.get("/groups/newest/")
        self.assertRedirects(response, "/groups/newest/1/")
        
        response = self.client.get("/groups/oldest/")
        self.assertRedirects(response, "/groups/oldest/1/")

        response = self.client.get("/groups/biggest/")
        self.assertRedirects(response, "/groups/biggest/1/")
        
        response = self.client.get("/groups/smallest/")
        self.assertRedirects(response, "/groups/smallest/1/")

    def test_users_group_page(self):
        #tests the page showing the list of a player's groups
        player = Player.objects.get(user__username="example_user")
        group_count = player.groups.count()
        response = self.client.get("/users/example_user/groups/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(len(soup.find_all("span", class_="group")), group_count)

    def test_group_page(self):
        group = Group.objects.get(slug="testers")
        member_count = group.members.count()
        response = self.client.get("/groups/testers/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(len(list(soup.find("table").find_all("tr")))-1, member_count)

    def test_newest(self):
        response = self.client.get("/groups/newest/1/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(soup.find("span", class_="group").a.text, "Galcon Book Club")

    def test_oldest(self):
        response = self.client.get("/groups/oldest/1/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(soup.find("span", class_="group").a.text, "Testers")

    def test_biggest(self):
        response = self.client.get("/groups/biggest/1/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(soup.find("span", class_="group").a.text, "Testers")

    def test_smallest(self):
        response = self.client.get("/groups/smallest/1/")
        soup = soupify(response.content.decode("utf8"))
        self.assertEqual(soup.find("span", class_="group").a.text, "Galcon Book Club")
    

class Test_Create_Group(My_Test_Case):
    fixtures = ["users.json", "groups.json"]

    def setUp(self):
        self.client.post("/login/", {"username": "example_user",
                                        "password": "password"})
    def test_template(self):
        response = self.client.get("/groups/new/")
        self.assertTemplateUsed("modify_group.html")
        
    def test_success(self):
        old_count = Group.objects.count()
        response = self.client.post("/groups/new/", {"name": "Test",
                                                     "description": "this is a test",
                                                     "join_requires_approval": False})
        new_group = Group.objects.get(slug="test")
        self.assertEqual(Group.objects.count(), old_count + 1)
        self.assertEqual(new_group.name, "Test")
        self.assertEqual(len(new_group.owners), 1)
        self.assertEqual(new_group.owners.all()[0].user.username, "example_user")
        self.assertEqual(len(new_group.members.all()), 1)
        self.assertEqual(new_group.members.all()[0].user.username, "example_user")
        self.assertEqual(new_group.description, "this is a test")
        self.assertFalse(new_group.hidden)
        self.assertFalse(new_group.join_requires_approval)

        
"""class Test_Delete_Group(My_Test_Case):
    fixtures = ["users.json", "groups.json"]
    def setUp(self):
        self.group = """

class Test_Change_Group_Membership(My_Test_Case):
    fixtures = ["users.json", "groups.json"]
    def setUp(self):
        self.client.post("/login/", {"username": "friendless_user",
                                "password": "password"})
        response = self.client.post("/groups/new/", {"name": "Test",
                                             "description": "this is a test",
                                             "join_requires_approval": False})

        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                                     "password": "password"})
        
        self.client.post("/groups/test/join/", {"username": "example_user"})
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "friendless_user",
                                "password": "password"})
        self.client.post("/groups/test/admins/", {"username": "example_user",
                                                  "adminship": "admin"})
        #Obviously, the "Test" has only one member: friendless_user
        #It's obviously admined by friendless_user
        self.test_group = Group.objects.get(slug="test")

        #Testers has three members: example_user, friendless_user, and only_friend
        #It's admined by example_user and friendless_user
        self.testers_group = Group.objects.get(slug="testers")
        
        #the book club has two members: example_user and only_friend
        #It's admined by example_user
        self.book_club_group = Group.objects.get(slug="galcon_book_club")

    def test_join_group(self):
        old_member_count = self.book_club_group.members.count()
        player = Player.objects.get(user__username="friendless_user")
        
        self.assertFalse(player in self.book_club_group.members.all())

        self.client.post("/groups/galcon_book_club/join/", {"username": "friendless_user"})
        self.assertEqual(self.book_club_group.members.count(), old_member_count + 1)
        
        self.assertTrue(player in self.book_club_group.members.all())

    def test_leave_group(self):
        old_member_count = self.testers_group.members.count()
        self.client.post("/groups/testers/leave/", {"username": "friendless_user"})
        self.assertEqual(self.testers_group.members.count(), old_member_count - 1)

    def test_remove_member_success(self):
        print("Starting successful removal test")
        old_member_count = self.test_group.members.count()
        
        self.client.post("/groups/test/", {"username": "example_user",
                                           "action": "remove"})
        self.assertEqual(self.test_group.members.count(), old_member_count - 1)
        print("finished test")
    def test_nonsuperadmin_remove_member_failure(self):

        old_member_count = self.testers_group.members.count()
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "only_friend",
                                     "password": "password"})
        
        self.client.post("/groups/test/join/", {"username": "only_friend"})
        self.client.get("/logout/")

        self.client.post("/login/", {"username": "example_user",
                             "password": "password"})

        self.client.post("/groups/test/", {"username": "only_friend",
                                           "action": "remove"})
        self.assertEqual(self.testers_group.members.count(), old_member_count)
    def test_superadmin_remove_member(self):
        self.client.post("/groups/test/admins/", {"username": "example_user",
                                                  "adminship": "superadmin"})
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "only_friend",
                             "password": "password"})
        self.client.post("/groups/test/join/", {"username": "only_friend"})
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                     "password": "password"})

        old_member_count = self.test_group.members.count()
        self.client.post("/groups/test/", {"username": "only_friend",
                                           "action": "remove"})
        self.assertEqual(self.test_group.members.count(), old_member_count - 1)

    def test_remove_someone_above_failure(self):
        old_member_count = self.testers_group.members.count()
        self.client.post("/groups/test/admins/", {"username": "example_user",
                                          "adminship": "superadmin"})
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                     "password": "password"})
        self.client.post("/groups/test/", {"username": "friendless_user",
                                   "action": "remove"})
        self.assertEqual(self.testers_group.members.count(), old_member_count)
        

class Test_Change_Adminship(My_Test_Case):
    fixtures = ["users.json", "groups.json"]
    
    def setUp(self):
        self.client.post("/login/", {"username": "friendless_user",
                                "password": "password"})
        response = self.client.post("/groups/new/", {"name": "Test",
                                             "description": "this is a test",
                                             "join_requires_approval": False})
        #Obviously, the "Test" has only one member: friendless_user
        #It's obviously admined by friendless_user
        self.test_group = Group.objects.get(slug="test")

        #Testers has three members: example_user, friendless_user, and only_friend
        #It's admined by example_user and friendless_user
        self.testers_group = Group.objects.get(slug="testers")
        
        #the book club has two members: example_user and only_friend
        #It's admined by example_user
        self.book_club_group = Group.objects.get(slug="galcon_book_club")
    def test_remove_last_admin(self):
        #Makes sure that nothing happens when some action is taken that would
        #result in a group without an owner
        self.client.get("/logout/")
        old_member_count = self.book_club_group.members.count()
        old_owner_count = self.book_club_group.owners.count()
        self.client.post("/login/", {"username": "example_user",
                                "password": "password"})
        self.client.post("/groups/galcon_book_club/leave/", {"username": "friendless_user"})
        self.assertEqual(self.book_club_group.members.count(), old_member_count)
        self.assertEqual(self.book_club_group.owners.count(), old_owner_count)

    def test_lower_last_owner(self):
        print("testing lower")
        old_owner_count = self.test_group.owners.count()
        self.client.post("/groups/test/admins/", {"username": "friendless_user",
                                                              "adminship": "none"})
        self.assertEqual(self.test_group.owners.count(), old_owner_count)

    def test_admin_above(self):
        #Tests the case where a player tries to push another player to an admin level
        #above his own
        old_admin_count = self.testers_group.admins.count()
        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                          "adminship": "superadmin"})
        self.assertEqual(self.testers_group.admins.count(), old_admin_count)

    def test_admin_same_level(self):
        #This should fail.
        
        old_admin_count = self.testers_group.admins.count()
        
        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                          "adminship": "admin"})

        self.assertEqual(self.testers_group.admins.count(), old_admin_count)

    def test_admin_self(self):
        #Tests the silly case where a player tries to push himelf up an admin level

        old_owner_count = self.testers_group.owners.count()
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                                          "adminship": "owner"})
        self.assertEqual(self.testers_group.owners.count(), old_owner_count)

    def test_deadmin_self(self):
        old_admin_count = self.testers_group.admins.count()
        
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                                     "adminship" : "none"})

        self.assertEqual(self.testers_group.admins.count(), old_admin_count - 1)
        
    def test_deadmin_above(self):
        #Tests deadmining someone above a user's admin level
        #(Which should fail and do nothing)

        #Example_user is owner and friendless_user is admin

        old_admin_count = self.testers_group.admins.count()
        
        self.client.post("/groups/testers/admins/", {"username": "example_user",
                                                     "adminship": "none"})
        
        self.assertEqual(self.testers_group.admins.count(), old_admin_count)

    def test_deadmin_same_level(self):
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        old_admin_count = self.testers_group.admins.count()

        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                  "adminship": "admin"})
        
        self.assertEqual(self.testers_group.admins.count(), old_admin_count + 1)
        
        self.client.get("/logout/")

        self.client.post("/login/", {"username": "friendless_user",
                "password": "password"})

        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                     "adminship": "none"})

        self.assertEqual(self.testers_group.admins.count(), old_admin_count + 1)
        
    def test_deadmin_below(self):
        #Tests deadmining someone below a user's admin level
        
        #We have to change accounts because we don't want to test unadmining
        #ourselves
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        old_admin_count = self.testers_group.admins.count()
        
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                                     "adminship": "none"})

        self.assertEqual(self.testers_group.admins.count(), old_admin_count - 1)

    def test_lower_admin_above(self):
        #Tests lowering someone with a higher admin level than the current user
        #(But not removing adminship altogether)
        #(This should fail)
        
        old_owner_count = self.testers_group.owners.count()
        self.client.post("/groups/testers/admins/", {"username": "example_user",
                                                          "adminship": "admin"})
        self.assertEqual(self.testers_group.owners.count(), old_owner_count)

    def test_lower_admin_same_level(self):
        #This should fail
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        old_superadmin_count = self.testers_group.superadmins.count()

        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                  "adminship": "superadmin"})
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                          "adminship": "superadmin"})

        self.assertEqual(self.testers_group.superadmins.count(), old_superadmin_count + 2)
        
        self.client.get("/logout/")
        
        self.client.post("/login/", {"username": "friendless_user",
                        "password": "password"})

        self.client.post("/groups/testers/admins/", {"username": "only_friend",
                                                  "adminship": "admin"})

        self.assertEqual(self.testers_group.superadmins.count(), old_superadmin_count + 2)

    def test_lower_admin_below(self):
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        old_superadmin_count = self.testers_group.superadmins.count()
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                  "adminship": "superadmin"})
        self.assertEqual(self.testers_group.superadmins.count(), old_superadmin_count + 1)
        
        self.client.post("/groups/testers/admins/", {"username": "friendless_user",
                                  "adminship": "admin"})
        self.assertEqual(self.testers_group.superadmins.count(), old_superadmin_count) 

class Test_Requests(My_Test_Case):
    fixtures = ["users.json", "groups.json"]
    def setUp(self):
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})
        response = self.client.post("/groups/new/", {"name": "Test",
                                             "description": "this is a test",
                                             "join_requires_approval": True})
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "friendless_user",
                                     "password": "password"})
        self.test_group = Group.objects.get(slug="test")

    def test_join_request_sent(self):
        old_join_request_count = self.test_group.join_group_requests.count()
        self.client.post("/groups/test/join/", {"username": "friendless_user"})
        self.assertEqual(self.test_group.join_group_requests.count(), old_join_request_count + 1)

    def test_join_request_accepted(self):
        old_member_count = self.test_group.members.count()
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()
        self.client.post("/groups/test/join/", {"username": "friendless_user"})
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count + 1)
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()
        old_join_request_count = self.test_group.join_group_requests.count()

        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        self.client.post("/groups/test/requests/", {"username": "friendless_user",
                                                    "action": "accept"})
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count - 1)
        self.assertEqual(self.test_group.join_group_requests.count(), old_join_request_count - 1)
        self.assertEqual(self.test_group.members.count(), old_member_count + 1)

    def test_friend_request_rejected(self):
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()
        old_rejected_join_request_count = self.test_group.join_group_requests.filter(accepted=False).count()
        old_member_count = self.test_group.members.count()
        self.client.post("/groups/test/join/", {"username": "friendless_user"})
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count + 1)
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()

        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})
        
        self.client.post("/groups/test/requests/", {"username": "friendless_user",
                                                    "action": "block"})
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count - 1)
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=False).count(), old_rejected_join_request_count + 1)
        self.assertEqual(self.test_group.members.count(), old_member_count)

    def test_friend_request_ignored(self):
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()
        old_member_count = self.test_group.members.count()
        print("A member", self.test_group.members.count())
        self.client.post("/groups/test/join/", {"username": "friendless_user"})
        print("B member", self.test_group.members.count())
        old_join_request_count = self.test_group.join_group_requests.count()
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count + 1)
        old_unread_join_request_count = self.test_group.join_group_requests.filter(accepted=None).count()

        self.client.get("/logout/")
        print("C member", self.test_group.members.count())
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})
        print("D member", self.test_group.members.count())
        
        self.client.post("/groups/test/requests/", {"username": "friendless_user",
                                                    "action": "ignore"})

        print("E member", self.test_group.members.count())
 
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=None).count(), old_unread_join_request_count - 1)
        self.assertEqual(self.test_group.join_group_requests.count(), old_join_request_count - 1)
        self.assertEqual(self.test_group.members.count(), old_member_count)

    def test_block_member(self):
        self.client.post("/groups/test/join/", {"username": "friendless_user"})
        
        old_rejected_join_request_count = self.test_group.join_group_requests.filter(accepted=False).count()
        self.client.get("/logout/")
        self.client.post("/login/", {"username": "example_user",
                        "password": "password"})

        self.client.post("/groups/test/requests/", {"username": "friendless_user",
                                                    "action": "accept"})
        old_member_count = self.test_group.members.count()
        print("Here, ", old_member_count, "should be 2")
        self.client.post("/groups/test/", {"username": "friendless_user",
                                                    "action": "block"})
        self.assertEqual(self.test_group.members.count(), old_member_count - 1)
        self.assertEqual(self.test_group.join_group_requests.filter(accepted=False).count(), old_rejected_join_request_count + 1)

        
        
        
