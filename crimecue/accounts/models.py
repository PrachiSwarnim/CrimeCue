from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        lat = f"{self.latitude}" if self.latitude is not None else "N/A"
        lon = f"{self.longitude}" if self.longitude is not None else "N/A"
        
        return f"{self.username} (Lat: {self.latitude}, Lon: {self.longitude})"