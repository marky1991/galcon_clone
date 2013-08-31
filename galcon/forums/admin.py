from django.contrib import admin

from .models import Section, Subsection, Thread, Post

class SubsectionInline(admin.TabularInline):
    model = Subsection

class SectionAdmin(admin.ModelAdmin):
    inlines = [SubsectionInline]

class ThreadInline(admin.TabularInline):
    model = Thread

class SubsectionAdmin(admin.ModelAdmin):
    inlines = [ThreadInline]

class PostInline(admin.TabularInline):
    model = Post

class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostInline]

    def save_model(self, request, obj, form, *args, **kwargs):
        return
    def save_formset(self, request, form, formset, change):
        #print(dir(formset), form, formset.forms, "FORMSET")
        form_data = cleanup_attribs(form.data)

        if formset.is_valid():
            data = cleanup_attribs(formset.data)
            posts = []
            def try_int(x):
                try:
                    return int(x)
                except ValueError:
                    return float("inf")
            keys = sorted(list(data.keys()), key=lambda x: try_int(x))
            for key in keys:
                try:
                    int(key)
                except ValueError:
                    continue
                
                posts.append(Post.prepare(title=data[key]["title"],
                                  text=data[key]["text"],
                                  author=data[key]["author"],
                                  #data[key]["post_date"]
                                  post_date=timezone.now()))
            thread = Thread.create(post=posts[0], **form_data)

            thread.save()
            for post in posts[1:]:
                try:
                    post(thread).full_clean()
                    post(thread).save()
                except ValueError:
                    pass

admin.site.register(Post)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subsection, SubsectionAdmin)
admin.site.register(Thread, ThreadAdmin)
    
