from django.contrib import admin
from .models import Announcement, Message


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'event', 'sent_at')
    search_fields = ('subject', 'content')
