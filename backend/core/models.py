from django.db import models

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    host = models.CharField(max_length=255, blank=True, default="")
    scheduled_date = models.DateField(null=True, blank=True)
    duration_mins = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("scheduled", "Scheduled"), ("live", "Live"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="scheduled")
    participants = models.IntegerField(default=0)
    meeting_url = models.URLField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    meeting_title = models.CharField(max_length=255, blank=True, default="")
    role = models.CharField(max_length=50, choices=[("host", "Host"), ("co_host", "Co Host"), ("presenter", "Presenter"), ("attendee", "Attendee")], default="host")
    joined = models.BooleanField(default=False)
    duration_mins = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Recording(models.Model):
    title = models.CharField(max_length=255)
    meeting_title = models.CharField(max_length=255, blank=True, default="")
    duration_mins = models.IntegerField(default=0)
    size_mb = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("processing", "Processing"), ("ready", "Ready"), ("expired", "Expired")], default="processing")
    download_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
