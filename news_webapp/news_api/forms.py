from django import forms
from django.contrib.auth.forms import UserCreationForm
# creating a form 
class SignupForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        # self.fields["password1"].widget.attrs["class"] = "form-control"
        # self.fields["password2"].widget.attrs["class"] = "form-control"

    def username(self):
        username = self.cleaned_data['username']
        return username

    def password1(self):
        password1 = self.cleaned_data['password']
        return password1

    
    def password2(self):
        password2 = self.cleaned_data['password']
        return password2