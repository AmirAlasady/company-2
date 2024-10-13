from django.db import models
from root.models import User

class PrivateRoom(models.Model):
    name = models.CharField(max_length=255)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_rooms')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_rooms')
    room_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user1} and {self.user2}"

class PrivateMessage(models.Model):
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.message}"
    



class Notification(models.Model):
    description = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender}: {self.recipient}: {self.description}"


    