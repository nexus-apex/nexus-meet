from django.contrib import admin
from .models import Meeting, Participant, Recording

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ["title", "host", "scheduled_date", "duration_mins", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "host"]

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "meeting_title", "role", "joined", "created_at"]
    list_filter = ["role"]
    search_fields = ["name", "email", "meeting_title"]

@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ["title", "meeting_title", "duration_mins", "size_mb", "date", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "meeting_title"]
