from django.db import models
from django.contrib.auth.models import User
import secrets


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    lake = models.ForeignKey(
        'lakes_app.Lake', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='events'
    )
    location = models.CharField(max_length=300)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    required_materials = models.TextField(
        blank=True, help_text="List materials volunteers should bring, one per line"
    )
    max_volunteers = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    event_code = models.CharField(max_length=16, unique=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.event_code:
            self.event_code = 'CLT-' + secrets.token_hex(4).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def registered_count(self):
        return self.registrations.filter(status='registered').count()

    def is_full(self):
        return self.registered_count() >= self.max_volunteers

    def spots_left(self):
        return max(0, self.max_volunteers - self.registered_count())


class EventRole(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_volunteers = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.event.title} — {self.name}"


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('cancelled', 'Cancelled'),
    ]
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    role = models.ForeignKey(EventRole, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    hours_logged = models.FloatField(default=0)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('volunteer', 'event')

    def __str__(self):
        return f"{self.volunteer.username} — {self.event.title}"


class WorkLog(models.Model):
    registration = models.OneToOneField(
        EventRegistration, on_delete=models.CASCADE, related_name='work_log'
    )
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)

    def duration_display(self):
        if self.duration_minutes is not None:
            hours = self.duration_minutes // 60
            mins = self.duration_minutes % 60
            if hours and mins:
                return f"{hours}h {mins}m"
            elif hours:
                return f"{hours}h"
            return f"{mins}m"
        return None

    def __str__(self):
        return f"{self.registration.volunteer.username} @ {self.registration.event.title}"
