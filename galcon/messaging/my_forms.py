from django import forms

from .models import Pm

class Modify_Message_Form(forms.ModelForm):
    class Meta:
        model = Pm
        fields = ["title", "text"]
