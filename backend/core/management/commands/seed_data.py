from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Meeting, Participant, Recording
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusMeet with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusmeet.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Meeting.objects.count() == 0:
            for i in range(10):
                Meeting.objects.create(
                    title=f"Sample Meeting {i+1}",
                    host=f"Sample {i+1}",
                    scheduled_date=date.today() - timedelta(days=random.randint(0, 90)),
                    duration_mins=random.randint(1, 100),
                    status=random.choice(["scheduled", "live", "completed", "cancelled"]),
                    participants=random.randint(1, 100),
                    meeting_url=f"https://example.com/{i+1}",
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Meeting records created'))

        if Participant.objects.count() == 0:
            for i in range(10):
                Participant.objects.create(
                    name=f"Sample Participant {i+1}",
                    email=f"demo{i+1}@example.com",
                    meeting_title=f"Sample Participant {i+1}",
                    role=random.choice(["host", "co_host", "presenter", "attendee"]),
                    joined=random.choice([True, False]),
                    duration_mins=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 Participant records created'))

        if Recording.objects.count() == 0:
            for i in range(10):
                Recording.objects.create(
                    title=f"Sample Recording {i+1}",
                    meeting_title=f"Sample Recording {i+1}",
                    duration_mins=random.randint(1, 100),
                    size_mb=round(random.uniform(1000, 50000), 2),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["processing", "ready", "expired"]),
                    download_url=f"https://example.com/{i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Recording records created'))
