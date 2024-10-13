from django.db import models
from root.models import User
# Create your models here.

class todoemployee(models.Model):
    task=models.CharField(max_length=500)
    date_Created=models.DateField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='his_tasks')
    done=models.BooleanField(default=False)
    by_ceo=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.task


class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/files/')  # Directory where files will be uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_files')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_files')

    def __str__(self):
        return f'{self.owner} | {self.title}'

class reports(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/reports/')  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f' report: {self.title} | {self.uploaded_at}'