from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.conf import settings

class GradeLevel(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False) 
    name = models.CharField(max_length=50, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class Topic(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False, related_name='topics')
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class SubTopic(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False, related_name='subtopics')
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class Prompt(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name

def worksheet_upload_path(instance, filename):
    # Generate filename based only on instance data
    base_filename = f"worksheet_{instance.id}_{instance.created_at.strftime('%Y%m%d_%H%M%S')}"
    # Determine extension based on field name rather than original filename
    if 'pdf' in filename:
        ext = 'pdf'
    else:
        ext = 'docx'
    return f'worksheets/{instance.user.id}/{base_filename}.{ext}'

class Sheet(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, blank=False, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False, related_name='sheets')
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, blank=False, null=False, related_name='sheets')
    title = models.CharField(max_length=200, blank=False, null=False)
    published = models.BooleanField(default=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    true_false_count = models.IntegerField(default=0, blank=False, null=False)
    multiple_choice_count = models.IntegerField(default=0, blank=False, null=False)
    fill_in_the_blank_count = models.IntegerField(default=0, blank=False, null=False)
    short_answer_count = models.IntegerField(default=0, blank=False, null=False)
    include_answer_key = models.BooleanField(default=True, blank=False, null=False)
    docx_file = models.FileField(upload_to=worksheet_upload_path, null=True, blank=True)
    pdf_file = models.FileField(upload_to=worksheet_upload_path, null=True, blank=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField()
    parent_sheet = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='versions')
    version_number = models.IntegerField(default=1)

    @property
    def like_count(self):
        return self.likes.count()
    

class SavedSheet(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'sheet') # Prevent duplicate saves

class LikedSheet(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, related_name='likes', blank=False, null=False)

    class Meta:
        unique_together = ('user', 'sheet') # Prevent duplicate likes

class Review(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, related_name='reviews', blank=False, null=False)
    rating = models.IntegerField(blank=False, null=False, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        unique_together = ('user', 'sheet') # Prevent duplicate reviews
    
