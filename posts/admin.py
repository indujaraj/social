from django.contrib import admin

from posts.models import Post, Comment, ThreadModel, MessageModel


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'image', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment']


@admin.register(ThreadModel)
class ThreadModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'receiver']


@admin.register(MessageModel)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['thread', 'sender_user', 'receiver_user', 'body', 'image']
