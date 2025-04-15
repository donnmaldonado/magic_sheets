from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class SubTopic(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

def worksheet_upload_path(instance, filename):
    # Generates path such as: worksheets/user_id/YYYY-MM-DD/filename
    return f'worksheets/{instance.creator.id}/{instance.created_at.strftime("%Y-%m-%d")}/{filename}'

class Prompt(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    
class Sheet(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, blank=False, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False)
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=50, blank=False, null=False)
    published = models.BooleanField(default=False, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False, null=False)
    true_false_count = models.IntegerField(default=0, blank=False, null=False)
    multiple_choice_count = models.IntegerField(default=0, blank=False, null=False)
    fill_in_the_blank_count = models.IntegerField(default=0, blank=False, null=False)
    short_answer_count = models.IntegerField(default=0, blank=False, null=False)
    include_answer_key = models.BooleanField(default=False, blank=False, null=False)
    docx_file = models.FileField(upload_to=worksheet_upload_path, null=True, blank=True)
    pdf_file = models.FileField(upload_to=worksheet_upload_path, null=True, blank=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, blank=False, null=False)

    def get_worksheet_filename(self):
        """Generate a filename for the worksheet"""
        return f"worksheet_{self.id}_{self.created_at.strftime('%Y%m%d_%H%M%S')}.docx"
    
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
    
