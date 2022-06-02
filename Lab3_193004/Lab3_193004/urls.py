"""Lab3_193004 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from Blog.views import block_user, frontpage, post_detail, write_post, profile_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/', frontpage, name='frontpage'),
    path('add/post/', write_post, name='write_post'),
    path('profile/', profile_view, name='profile_view'),
    path('blockedUsers/', block_user, name='block_user'),
    path('admin/', admin.site.urls),
    path('<slug:slug>/', post_detail, name='post_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

