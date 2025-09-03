from webbrowser import get
from django.db.models.signals import post_save
from django.dispatch import receiver
from crime_data.models import CrimeRecord
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=CrimeRecord)
def send_crime_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "crimes",
            {
                "type": "send_crime",
                "crime": {
                    "crime_type": instance.crime_type,
                    "description": instance.descriptions,
                    "lat": float(instance.location_latitude),
                    "lon": float(instance.location_longitude),
                    "timestamp": instance.timestamp.isoformat()
                }
            }
        )