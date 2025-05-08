from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Topic, SubTopic, Prompt, Sheet, Review

@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    list_display = ('name', 'subject', 'grade_level')
    list_filter = ('subject', 'grade_level')
    search_fields = ('name', 'subject__name')

@admin.register(SubTopic)
class SubTopicAdmin(ImportExportModelAdmin):
    list_display = ('name', 'topic')
    list_filter = ('topic__subject', 'topic__grade_level')
    search_fields = ('name', 'topic__name')

@admin.register(Prompt)
class PromptAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'text')

@admin.register(Sheet)
class SheetAdmin(ImportExportModelAdmin):
    list_display = ('title', 'subject', 'grade_level', 'topic', 'sub_topic', 'created_at', 'updated_at')
    list_filter = ('subject', 'grade_level', 'topic', 'sub_topic')
    search_fields = ('title', 'subject__name', 'grade_level__name', 'topic__name', 'sub_topic__name')

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('user', 'sheet', 'rating', 'comment', 'created_at')
    list_filter = ('user', 'sheet', 'rating')
    search_fields = ('user__username', 'sheet__title', 'comment')

