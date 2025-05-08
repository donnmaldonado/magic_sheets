from django.contrib import admin
from .models import Subject, Topic, SubTopic, Prompt

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'grade_level')
    list_filter = ('subject', 'grade_level')
    search_fields = ('name', 'subject__name')

@admin.register(SubTopic)
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic')
    list_filter = ('topic__subject', 'topic__grade_level')
    search_fields = ('name', 'topic__name')

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'text')
