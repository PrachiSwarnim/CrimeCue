from django.db import models
from django.utils import timezone

class Notification(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read =  models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.created_at}"