from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.contrib import admin

from galcon.models import Player, Rank, Trophy

included_models = [Player, Rank, Trophy]

for model in included_models:
    admin.site.register(model)

class UserProfileInline(admin.StackedInline):
    model = Player

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

def cleanup_attribs(queryset):
    new_dict = {}
    for key, value in queryset.items():
        item_num = None
        try:
            var_name, item_num, attribute = key.split("-")
            if item_num not in new_dict:
                new_dict[item_num] = {} 
        except ValueError:
            attribute = key
        if attribute == "author" or attribute == "parent":
            if attribute == "author":
                cls = Player
            else:
                cls = Subsection
            if value == "":
                value = None
            else:
                value = cls.objects.get(id=int(value))
        if item_num is not None:
            new_dict[item_num][attribute] = value
        else:
            new_dict[attribute] = value
    return new_dict
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
