from django import forms
from .models import Post

class Modify_Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text"]

Edit_Post_Form = Create_Post_Form = Modify_Post_Form

Create_Thread_Form = Modify_Post_Form
