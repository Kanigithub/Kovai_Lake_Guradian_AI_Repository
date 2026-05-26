from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventRegistration, EventRole, WorkLog
from .forms import EventForm, EventRoleForm, EventRegistrationForm


def event_list(request):
    status_filter = request.GET.get('status', '')
    events = Event.objects.select_related('lake')
    if status_filter:
        events = events.filter(status=status_filter)
    else:
        events = events.order_by('date')
    return render(request, 'events_app/event_list.html', {
        'events': events,
        'status_filter': status_filter,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    roles = event.roles.all()
    user_registration = None
    user_work_log = None
    if request.user.is_authenticated:
        user_registration = EventRegistration.objects.filter(
            volunteer=request.user, event=event
        ).first()
        if user_registration:
            user_work_log = getattr(user_registration, 'work_log', None)
    registrations = event.registrations.exclude(status='cancelled').select_related(
        'volunteer', 'role'
    ).prefetch_related('work_log')
    return render(request, 'events_app/event_detail.html', {
        'event': event,
        'roles': roles,
        'user_registration': user_registration,
        'user_work_log': user_work_log,
        'registrations': registrations,
    })


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.is_full():
        messages.warning(request, 'Sorry, this event is full.')
        return redirect('events_app:event_detail', pk=pk)
    existing = EventRegistration.objects.filter(volunteer=request.user, event=event).first()
    if existing:
        messages.info(request, 'You are already registered for this event.')
        return redirect('events_app:event_detail', pk=pk)
    if request.method == 'POST':
        form = EventRegistrationForm(event, request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.volunteer = request.user
            reg.event = event
            reg.save()
            # Award first-event badge if needed
            _check_and_award_badge(request.user)
            messages.success(request, f'You have successfully registered for "{event.title}"!')
            return redirect('events_app:event_detail', pk=pk)
    else:
        form = EventRegistrationForm(event)
    return render(request, 'events_app/event_register.html', {'event': event, 'form': form})


@login_required
def event_cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg = get_object_or_404(EventRegistration, volunteer=request.user, event=event)
    if request.method == 'POST':
        reg.status = 'cancelled'
        reg.save()
        messages.info(request, 'Your registration has been cancelled.')
        return redirect('events_app:event_detail', pk=pk)
    return render(request, 'events_app/event_cancel_confirm.html', {'event': event})


@login_required
def event_create(request):
    if not request.user.userprofile.is_organizer:
        messages.error(request, 'Only organizers can create events.')
        return redirect('events_app:event_list')
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully.')
            return redirect('events_app:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events_app/event_create.html', {'form': form})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.userprofile.is_organizer:
        messages.error(request, 'Only organizers can edit events.')
        return redirect('events_app:event_detail', pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('events_app:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events_app/event_edit.html', {'form': form, 'event': event})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.userprofile.is_organizer:
        messages.error(request, 'Only organizers can delete events.')
        return redirect('events_app:event_detail', pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('events_app:event_list')
    return render(request, 'events_app/event_delete_confirm.html', {'event': event})


@login_required
def check_in(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg = get_object_or_404(EventRegistration, volunteer=request.user, event=event, status='registered')
    work_log, _ = WorkLog.objects.get_or_create(registration=reg)
    if work_log.check_in_time:
        messages.info(request, 'You have already checked in.')
    else:
        work_log.check_in_time = timezone.now()
        work_log.save()
        messages.success(request, f'Check-in recorded at {work_log.check_in_time.strftime("%I:%M %p")}.')
    return redirect('events_app:event_detail', pk=pk)


@login_required
def check_out(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg = get_object_or_404(EventRegistration, volunteer=request.user, event=event, status='registered')
    work_log = get_object_or_404(WorkLog, registration=reg)
    if not work_log.check_in_time:
        messages.error(request, 'You must check in before checking out.')
    elif work_log.check_out_time:
        messages.info(request, 'You have already checked out.')
    else:
        work_log.check_out_time = timezone.now()
        delta = work_log.check_out_time - work_log.check_in_time
        work_log.duration_minutes = max(1, int(delta.total_seconds() / 60))
        work_log.save()
        reg.hours_logged = round(work_log.duration_minutes / 60, 2)
        reg.status = 'attended'
        reg.save()
        messages.success(request, f'Check-out recorded. Total duration: {work_log.duration_display()}.')
    return redirect('events_app:event_detail', pk=pk)


def _check_and_award_badge(user):
    from volunteers_app.models import Badge, VolunteerBadge, UserProfile
    count = EventRegistration.objects.filter(volunteer=user, status='registered').count()

    # Event-count milestone badges (legacy)
    badge_map = {1: 'first_event', 5: 'five_events', 10: 'ten_events'}
    badge_type = badge_map.get(count)
    if badge_type:
        badge = Badge.objects.filter(badge_type=badge_type).first()
        if badge:
            VolunteerBadge.objects.get_or_create(user=user, badge=badge)

    # Update points
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.total_points = count * 10
    profile.save()

    # Auto-award all point-threshold badges
    for badge in Badge.objects.filter(min_points__isnull=False):
        if profile.total_points >= badge.min_points:
            VolunteerBadge.objects.get_or_create(user=user, badge=badge)
