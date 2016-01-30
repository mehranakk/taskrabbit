from django import forms
from .models import MyUser, Task, Skill

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['display_name', 'skills']
       # widgets = {
       #         'skills': forms.ChoiceField(choices=Skill.objects.all())
       #     }

class NewProfileForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="Email", required=True)
    display_name = forms.CharField(label="Displaye Name", required=True)

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'category',]
