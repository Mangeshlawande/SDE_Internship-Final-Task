from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User




class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField();
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') # use Tuple for Build in form 


# class CustomLoginForm(AuthenticationForm):
#     # Optional: Add a custom field, e.g., remember me
#     remember_me = forms.BooleanField(required=False)

        
class TweetSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search Tweets")

