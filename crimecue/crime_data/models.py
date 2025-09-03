from django.db import models
from django.utils import timezone


class CrimeReport(models.Model):
    source = models.TextField()
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "crime_reports"   # ✅ correct mapping
        managed = False              # ✅ so Django doesn’t try to recreate it
        unique_together = ("source", "title")

    def __str__(self):
        return f"{self.title} ({self.city})"


class PipelineLog(models.Model):
    run_time = models.DateTimeField(default=timezone.now)
    source = models.TextField(blank=True, null=True)
    new_reports = models.IntegerField(default=0)
    status = models.TextField(default="success")

    class Meta:
        db_table = "pipeline_log"    # ✅ corrected table mapping
        managed = False              # ✅ prevent duplicate ownership

    def __str__(self):
        return f"{self.run_time} - {self.source} ({self.status})"
