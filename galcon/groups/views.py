from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.contrib import messages

from django.contrib.auth.models import User
from django.db.models import Count

from django.utils.translation import ugettext as _

from . import my_forms
from . import models

from galcon import settings
from galcon.models import Player

def groups(request, username=None, page_number=None, sorting_function=None):
    if sorting_function is not None and page_number is None:
        return HttpResponseRedirect("/groups/" + sorting_function + "/1/")
    group = None
    form = None
    if request.method == "GET":
        if username is not None:
            user = User.objects.get(username=username)
            groups = user.player.groups.all()
        else:
            if sorting_function is None:
                return HttpResponseRedirect("/groups/newest/1/")
            
        groups = models.Group.objects.filter(hidden=False)
        if sorting_function == "newest":
            groups = groups.order_by("-creation_time")
        elif sorting_function == "oldest":
            groups = groups.order_by("creation_time")
        elif sorting_function == "biggest":
            groups = groups.annotate(size=Count("members")).order_by("-size")
        elif sorting_function == "smallest":
            groups = groups.annotate(size=Count("members")).order_by("size")
        pages = Paginator(groups, settings.children_per_page)
        if page_number is not None:
            groups = pages.page(page_number)
    else:
        pass

    return render(request, "groups/groups.html", locals())

def group(request, group_name=None):
    user_is_admin = False
    is_admin = {}
    group = models.Group.objects.get(slug=group_name)
    players = list(group.members.all())
    print(players, "players")
    admins = group.admins.all()
    user_is_admin = request.user.player in group.admins.all()
    user_is_superadmin = request.user.player in group.superadmins.all()
    user_is_owner = request.user.player in group.owners.all()
    user_is_member = request.user.player in group.members.all()
    print("Hi")
    
    for player in players:
        is_admin[player] = _("Yes") if player in admins else "-"
    if request.method == "POST":
        player = Player.objects.get(slug=request.POST["username"])
        group = models.Group.objects.get(slug=group_name)
        if player in group.members.all():
            membership = models.Membership.objects.get(player=player, group=group)
        else:
            membership = models.Membership.objects.create(player=player, group=group, adminship="none")
        form = my_forms.Edit_Membership_Form(instance=membership)
        action = request.POST["action"]
        if action == "remove":
            try:
                form.instance.delete()
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True)
        elif action == "block":
            print("Blocking the player guy from group")
            block = models.Join_Group_Request(author=player, recipient=group, accepted=False)
            block.save()
            try:
                membership.delete()
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True)
        elif action == "leave":
            try:
                membership.delete()
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True)
    return render(request, "groups/group.html", locals())
@login_required
def modify_group(request, group_name=None, action=None):
    if request.method == "GET":
        if action == "new":  
            form = my_forms.Edit_Group_Form()
        elif action == "edit":
            group = get_object_or_404(models.Group, slug=group_name)
            form = my_forms.Edit_Group_Form(instance=group)
    else:
        if action == "new":
            form = my_forms.Edit_Group_Form(data=request.POST)
            now = timezone.now()
            form.instance.creation_time = now
            if form.is_valid():
                group = models.Group.create(admin=request.user.player, **form.cleaned_data)
                group.save()
            else:
                return render(request, "groups/modify_group.html", {"request": request,
                                                 "form": form})
        elif action == "edit":
            group = get_object_or_404(models.Group, name=request.POST["name"])
            form = my_forms.Edit_Group_Form(data=request.POST, instance=group)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/groups/" + form.instance.slug + "/")
            
        return HttpResponseRedirect("/groups/")
    return render(request, "groups/modify_group.html", {"request": request,
                                                 "form": form})

@login_required
def change_membership(request, group_name=None, action=None):

    #target_username = request.POST["username"]
    target_username = request.user.username
    player = request.user.player
    group = models.Group.objects.get(slug=group_name)
    try:
        target_player = group.members.get(slug=target_username)
        #Superadmins and up can kick players out (And you can always kick
        #yourself out), but we can't have a group without any owners
        if action == "leave":
            print("Action was leave")
            if player == target_player or player in group.superadmins.all():
                membership = models.Membership.objects.get(player=target_player,
                                                       group=group)
                try:
                    membership.delete()
                except ValidationError as e:
                    messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True, extra_tags="error")
                    
    except ObjectDoesNotExist:
        if action == "join":
            if not group.join_requires_approval:
                
                membership = models.Membership.objects.create(player=player,
                                group=group,
                                adminship="none")
                membership.save()
            else:
                join_request = models.Join_Group_Request(author=player,
                                                         recipient=group)
                join_request.save()
    #By urls.py, we can assume group_name is not None
    print("Redirecting to", "/groups/" + group_name + "/")
    return HttpResponseRedirect("/groups/" + group_name + "/")

@login_required
def change_adminship(request, group_name=None):
    group = models.Group.objects.get(slug=group_name)
    is_admin = {}
    admins = group.admins.all()
    players = group.members.all()
    user_is_admin = request.user.player in group.admins.all()
    user_is_superadmin = request.user.player in group.superadmins.all()
    user_is_owner = request.user.player in group.owners.all()
    user_is_member = request.user.player in group.members.all()
    for player in players:
        is_admin[player] = _("Yes") if player in admins else "-"
    
    if request.method == "POST":
        username = request.POST["username"]
        target_player = Player.objects.get(slug=username)
        target_membership = models.Membership.objects.get(player=target_player, group=group)
        admin_level = request.POST["adminship"]
        if admin_level not in ["none", "admin", "superadmin", "owner"]:
            raise TypeError(_("Invalid admin level."))
        my_data = {"adminship": admin_level,
                "player": target_player.id,
                "group": group.id}
        data = dict(request.POST)
        data.update(my_data)
        form = my_forms.Edit_Membership_Form(data, instance=target_membership)
        player = request.user.player
        player_membership = models.Membership.objects.get(player=player, group=group)
        #if player is a higher admin than the target player

        #Owners get to do anything

        if (models.rank_to_num[player_membership.adminship] > models.rank_to_num[target_membership.adminship] or
            player_membership.adminship == "owner" or player == target_player):
            if (models.rank_to_num[admin_level] < models.rank_to_num[player_membership.adminship] or
                player_membership.adminship == "owner"):
                form.instance.adminship = admin_level
                if form.is_valid():
                    form.save()
            else:
                messages.add_message(request,
                                    messages.ERROR, _("You cannot raise someone's adminship level" \
                                    "to or above your own"), fail_silently=True, extra_tags="error")
        form = my_forms.Edit_Membership_Form()
    
    return render(request, "groups/group_admins.html", locals())   


@login_required
def requests(request, group_name=None, kind=None):
    group = models.Group.objects.get(slug=group_name)
    if kind == "requests":
        template = "groups/group_requests.html"
        players = list(map(lambda membership: membership.author, group.join_group_requests.filter(accepted=None)))
    elif kind == "blocks":
        template = "groups/group_blocks.html"
        players = list(map(lambda membership: membership.author,group.join_group_requests.filter(accepted=False)))
    else:
        template = "groups/group.html"
    user_is_admin = False
    is_admin = {}
    admins = group.admins.all()
    user_is_admin = request.user.player in group.admins.all()
    user_is_superadmin = request.user.player in group.superadmins.all()
    user_is_owner = request.user.player in group.owners.all()
    user_is_member = request.user.player in group.members.all()
    print("Hi")
    
    for player in players:
        is_admin[player] = "Yes" if player in admins else "-"
    print(players, "playerS")
    if request.method == "POST":
        print(request.POST)
        player = Player.objects.get(slug=request.POST["username"])
        print("1 member", group.members.count())
        if player in group.members.all():
            membership = models.Membership.objects.get(player=player, group=group)
        else:
            membership = models.Membership(player=player, group=group, adminship="none")
        #form = my_forms.Edit_Membership_Form(instance=membership)
        action = request.POST["action"]
        print("2 member", group.members.count())
        join_request = group.join_group_requests.get(author=player, recipient=group)
        if action == "accept":
            print("Accepting")
            print("Membershi[p: ", membership)
            membership.save()
            join_request.delete()
            print("Deleted the request")
        elif action == "ignore":
            try:
                print("3 member", group.members.count())
                join_request.delete()
                #membership.delete()
                #form.instance.delete()
                print("Successfully ignored")
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True, extra_tags="error")
        elif action == "block":
            print("blocking from requests")
            join_request.accepted = False
            join_request.save()
        elif action == "unblock":
            pass
        elif action == "leave":
            try:
                membership.delete()
            except ValidationError as e:
                messages.add_message(request, messages.ERROR, _(e.message), fail_silently=True, extra_tags="error")
    return render(request, template, locals())
        
