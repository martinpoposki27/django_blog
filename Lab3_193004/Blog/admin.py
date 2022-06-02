from urllib import request
from django.contrib import admin
from .models import BlockUser, Post, Blogger, Comment
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

class BlockUserAdmin(admin.ModelAdmin):
    exclude = ("userThatBlocks",)
    model = BlockUser
    
    def save_model(self, requset, obj, form, change):
        if getattr(obj, "userThatBlocks", None) is None:
            obj.userThatBlocks = requset.user
        return super().save_model(requset, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj = None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.userThatBlocks != request.user:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj = None):
        if obj is not None and obj.userThatBlocks != request.user:
            return False
        else:
            return True
    
class BloggerAdmin(admin.ModelAdmin):
    model = Blogger
    
    def save_model(self, requset, obj, form, change):
        if getattr(obj, "user", None) is None:
            obj.user = requset.user
        return super().save_model(requset, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        elif obj is not None and obj.user == request.user:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        elif obj is not None and obj.user == request.user:
            return True
        else:
            return False

class BlogCommentAdmin(admin.StackedInline):
    model = Comment
    extra = 0 #za sto sluzi ova
    exclude = ("blogger",)

    def get_readonly_fields(self, request, obj=None):
        if obj == None or (obj != None and obj.blogger == request.user):
            return []
        return self.readonly_fields
        #za sto se koristi ova i kako funkcionira

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj = None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.blogger != request.user:
            return False
        else:
            return True

class BlogCommentAdminIndividual(admin.ModelAdmin):
    model = Comment
    extra = 0
    exclude = ("blogger", "post")

    def get_readonly_fields(self, request, obj=None):
        if obj == None or (obj != None and obj.blogger == request.user):
            return []
        return self.readonly_fields

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj = None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.blogger != request.user:
            return False
        else:
            return True
    

class BlogPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ("title", "blogger")
    list_filter = (('date_added', DateTimeRangeFilter),)
    search_fields = ("title", "body")
    exclude = ("blogger" ,)
    inlines = [BlogCommentAdmin]
    readonly_fields = [
        'blogger',
        'title',
        'slug',
        'intro',
        'body',
        'file',
        'date_added',
        'date_changed'
    ]

    def get_queryset(self, request):
        usersThatBlockedOurUser = BlockUser.objects.filter(blockedUser = request.user).values_list("userThatBlocks")
        qs = super(BlogPostAdmin, self).get_queryset(request)
        qs = qs.exclude(blogger__in = usersThatBlockedOurUser)
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if obj == None or (obj != None and obj.blogger == request.user):
            return []
        return self.readonly_fields

    def has_add_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def has_change_permission(self, request, obj=None):
    #     if obj is not None and obj.blogger != request.user:
    #         return False
    #     else:
    #         return True
    
    def has_delete_permission(self, request, obj = None):
        if obj is not None and obj.blogger != request.user:
            return False
        else:
            return True

    def save_model(self, requset, obj, form, change):
        if getattr(obj, "blogger", None) is None:
            obj.blogger = requset.user
            #obj.blogger = Blogger.objects.get(user = requset.user)
        return super().save_model(requset, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        comments = formset.save(commit = False)
        for comment in comments:
            comment.blogger = request.user
            comment.save()

admin.site.register(Post, BlogPostAdmin)
admin.site.register(BlockUser, BlockUserAdmin)
#admin.site.register(Comment, BlogCommentAdmin)
#admin.site.register(Post)
admin.site.register(Blogger, BloggerAdmin)
admin.site.register(Comment, BlogCommentAdminIndividual)
