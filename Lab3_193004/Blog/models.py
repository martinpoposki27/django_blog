from email.policy import default
from pickle import TRUE
from tkinter import CASCADE
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blogger(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_img = models.ImageField(default="profile_imgs/lank-profile.png", upload_to="profile_imgs/")
    interests = models.CharField(null=True, blank=True, max_length=200)
    skills = models.CharField(null=True, blank=True, max_length=200)
    occupation = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=255)
    blogger = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True)
    intro = models.CharField(max_length=100)
    body = models.TextField()
    file = models.FileField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta: 
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title + " - " + str(self.blogger)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    blogger = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['date_added']

    def __str__(self):
        return self.body + " - " + str(self.blogger)

class BlockUser(models.Model):
    userThatBlocks = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userThatBlocks')
    blockedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blockedUser')

    def __str__(self) -> str:
        return str(self.userThatBlocks) + " blocked " + str(self.blockedUser)






