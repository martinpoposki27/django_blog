from http.client import HTTPResponse
from multiprocessing import context
from turtle import title
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Blogger, Post, BlockUser
from .forms import CommentForm, PostForm, ProfileImgForm, BlockForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def frontpage(request):
    if 'q' in request.GET:
        q = request.GET['q']
        posts = Post.objects.filter(title__icontains=q)
    else:
        usersThatBlockedOurUser = BlockUser.objects.filter(blockedUser = request.user).values_list("userThatBlocks")
        posts = Post.objects.all()
        posts = posts.exclude(blogger__in = usersThatBlockedOurUser)
        posts = posts.exclude(blogger = request.user)
    context = {
        'posts': posts
    }
    return render(request, 'blog/frontpage.html', {'posts': posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    #post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.blogger = request.user
            comment.save()
            
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def write_post(request):
    #post = Post.objects.get(slug=slug)
    #post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.post = post
            post.blogger = request.user
            post.save()
            
            return redirect('profile_view')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})

def profile_view(request):
    # blogger = Blogger.objects.get(user = request.user)
    # if request.method == 'POST':
    #     form = ProfileImgForm(request.POST, request.FILES)

    #     if form.is_valid():
    #         f = form.save(commit=False)
    #         # blogger.profile_img = f
    #         f.save()
    #         return redirect('profile_view')
    # else:
    #     form = ProfileImgForm()
    user = request.user
    blogger = Blogger.objects.get(user = request.user)
    posts = Post.objects.all()
    posts = posts.filter(blogger = request.user)
    context = {
        'posts': posts,
        'blogger': blogger,
        # 'form': form
    }
    return render(request, 'blog/profile_details.html', context=context)

def block_user(request):

    blockedUsers = BlockUser.objects.filter(userThatBlocks = request.user)

    if request.method == 'POST':
        form = BlockForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.userThatBlocks = request.user
            post.save()
            
            return redirect('block_user')
    else:
        form = BlockForm()

    return render(request, 'blog/block_user.html', {'form': form, 'blockedUsers': blockedUsers})
