from django.db import models

# Create your models here.
class todoceo(models.Model):
    task=models.CharField(max_length=500)
    date_Created=models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.task
    


