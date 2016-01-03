from django import forms
from .models import MyUser

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['display_name', 'picture',]
