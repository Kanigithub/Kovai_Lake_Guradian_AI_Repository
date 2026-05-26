from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events_app.models import Event
from lakes_app.models import Lake
from dashboard_app.models import Announcement


def home(request):
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date')[:3]
    lakes = Lake.objects.all()
    context = {
        'upcoming_events': upcoming_events,
        'lakes': lakes,
    }
    return render(request, 'home.html', context)


@login_required
def announcements(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'announcements.html', {'announcements': announcements})
