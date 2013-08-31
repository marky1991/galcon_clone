from django import forms

from . import models

class Edit_Group_Form(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ["name", "description", "hidden", "join_requires_approval"]

class Get_Members_Form(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ["members"]
class Edit_Membership_Form(forms.ModelForm):
    class Meta:
        model = models.Membership
        exclude = []
    

        
