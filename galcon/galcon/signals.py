from .models import Player, User
from django.db.models import signals
import galcon

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

signals.post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")


"""def attach_post_to_thread(sender, instance, created, **kwargs):
    if isinstance(instance, Thread) and created:
        curried_post = instance._post
        post = curried_post(instance)
        post.save()
signals.post_save.connect(attach_post_to_thread, dispatch_uid="attach_post")"""
        
"""
if not galcon.url_to_id:
    for Type in [Section, Subsection, Thread]:
        for item in Type.objects.all():
            url = ""
            original_id = item.id
            instance = item
            url = instance.to_url() + "/" + url
            while hasattr(instance, "parent"):
                print(instance,instance.id, "INST")
                instance = instance.parent
                url = instance.to_url() + "/" + url
            galcon.url_to_id["forums/" + url] = original_id
    
"""
