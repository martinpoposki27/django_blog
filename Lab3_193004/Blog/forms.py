from asyncio.windows_events import NULL
from dataclasses import fields
from socket import fromshare
from urllib import request
from django import forms
from .models import Blogger, Comment, Post, BlockUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control comment-field"

    class Meta:
        model = Comment
        blogger = Blogger
        exclude = ["blogger", "post"]

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Post
        blogger = Blogger
        exclude = ['blogger',]

class BlockForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
    
    class Meta:
        model = BlockUser
        userThatBlocks = Blogger
        exclude = ['userThatBlocks',]

class ProfileImgForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileImgForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Blogger
        fields = ["profile_img",]