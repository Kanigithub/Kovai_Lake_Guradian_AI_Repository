from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ACCOUNT_TYPES = [
        ('individual', 'Individual Volunteer'),
        ('ngo', 'NGO / Organization'),
    ]
    ORG_TYPES = [
        ('environmental', 'Environmental NGO'),
        ('corporate', 'Corporate CSR Group'),
        ('educational', 'Educational Institution'),
        ('community', 'Community / Resident Group'),
        ('religious', 'Religious / Cultural Group'),
        ('government', 'Government Body'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='individual')
    is_organizer = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    availability_weekdays = models.BooleanField(default=False)
    availability_weekends = models.BooleanField(default=True)
    skills = models.CharField(
        max_length=300, blank=True,
        help_text="Comma-separated skills, e.g. Swimming, First Aid, Photography"
    )
    total_points = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # NGO / Organization fields
    organization_name = models.CharField(max_length=200, blank=True)
    organization_type = models.CharField(max_length=50, choices=ORG_TYPES, blank=True)
    organization_size = models.PositiveIntegerField(null=True, blank=True, help_text="Approximate number of members")
    organization_website = models.URLField(blank=True)
    organization_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def total_hours(self):
        from events_app.models import EventRegistration
        return sum(
            r.hours_logged for r in EventRegistration.objects.filter(volunteer=self.user)
            if r.hours_logged
        )


class Badge(models.Model):
    BADGE_TYPES = [
        ('first_event', 'First Event'),
        ('five_events', '5 Events Attended'),
        ('ten_events', '10 Events Attended'),
        ('lake_guardian', 'Lake Guardian'),
        ('team_player', 'Team Player'),
        ('eco_warrior', 'Eco Warrior'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPES, blank=True, default='')
    icon = models.CharField(max_length=60, default='fas fa-award')
    min_points = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Auto-award when a volunteer reaches this many points. Leave blank for manual-only.'
    )

    def __str__(self):
        return self.name


class VolunteerBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} — {self.badge.name}"
