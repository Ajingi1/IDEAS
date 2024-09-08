from django.contrib import admin
from .models import News, Announcement

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'image')
    search_fields = ('title',)
    list_filter = ('time',)
    fields = ('title', 'time', 'image', 'content')  # Include content in admin form

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'time')
    search_fields = ('title',)
    list_filter = ('time',)
    fields = ('title', 'time', 'content')  # Include content in admin form
