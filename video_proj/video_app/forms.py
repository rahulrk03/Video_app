from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo,Video

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')
        #fields = '__all__'

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name","description","categories","tags", "videofile"]
