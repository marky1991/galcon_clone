from django.contrib import admin

from .models import Group, Membership, Join_Group_Request

class Membership_Inline(admin.TabularInline):
    model = Membership
    extra = 5

class Join_Group_Request_Inline(admin.TabularInline):
    model = Join_Group_Request
    extra = 5

class Group_Admin(admin.ModelAdmin):
    inlines = (Membership_Inline, Join_Group_Request_Inline)

admin.site.register(Group, Group_Admin)
admin.site.register(Membership)
admin.site.register(Join_Group_Request)
