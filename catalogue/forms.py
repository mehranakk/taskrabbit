from django import forms
from .models import MyUser

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['display_name',]

class NewProfileForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="Email", required=True)
    display_name = forms.CharField(label="Displaye Name", required=True)
