from django.contrib.auth import forms as builtin_forms
from django import forms

from . import settings
"""g2alcontourneybattle2010@gmail.com
    HTWE9YMA"""

class Create_Account_Form(builtin_forms.UserCreationForm):
    email = forms.EmailField()
    registration_email = forms.EmailField()
    registration_code = forms.CharField()

class Player_Form(forms.Form):
    username = forms.CharField(max_length=settings.max_name_length)
    email = forms.EmailField()
    registration_email = forms.EmailField(required=False)
    registration_code = forms.CharField(max_length=settings.max_registration_code_length, required=False)

class Create_Player_Form(forms.Form):
    password1 = forms.CharField(max_length=settings.max_password_length)
    password2 = forms.CharField(max_length=settings.max_password_length)
    
class Edit_Profile_Form(Player_Form):
    password1 = forms.CharField(max_length=settings.max_password_length, required=False)
    password2 = forms.CharField(max_length=settings.max_password_length, required=False)
    location = forms.CharField(max_length=settings.max_location_length, required=False)
    avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data["password1"] != cleaned_data["password2"]:
            if "password1" in self._errors:
                self._errors["password1"].append(self.error_class(["The passwords must match."]))
            else:
                self._errors["password1"] = self.error_class(["The passwords must match."])
        return cleaned_data
