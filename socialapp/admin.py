from django.contrib import admin

from socialapp.models import Profile, Relationship


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','bio', 'gender', 'image']


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
