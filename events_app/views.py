from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Event, EventRegistration, EventRole, WorkLog
from .forms import EventForm, EventRoleForm, EventRegistrationForm


def event_list(request):
    tab = request.GET.get('tab', 'registered')
    upcoming_events = Event.objects.filter(status='upcoming').select_related('lake').order_by('date')
    completed_events = Event.objects.filter(status='completed').select_related('lake').order_by('-date')
    registered_events = Event.objects.none()
    volunteer_attended_events = Event.objects.none()

    if request.user.is_authenticated and not request.user.userprofile.is_organizer:
        # Events the volunteer has actively registered for (not yet attended / not cancelled)
        registered_events = Event.objects.filter(
            registrations__volunteer=request.user,
            registrations__status='registered',
            status='upcoming'
        ).select_related('lake').distinct().order_by('date')

        # Events the volunteer has checked out of (registration status = 'attended')
        volunteer_attended_events = Event.objects.filter(
            registrations__volunteer=request.user,
            registrations__status='attended'
        ).select_related('lake').distinct().order_by('-date')

        # Exclude both registered and personally-attended events from the general upcoming list
        exclude_ids = list(registered_events.values_list('id', flat=True)) + \
                      list(volunteer_attended_events.values_list('id', flat=True))
        upcoming_events = upcoming_events.exclude(id__in=exclude_ids)

    return render(request, 'events_app/event_list.html', {
        'registered_events': registered_events,
        'upcoming_events': upcoming_events,
        'completed_events': completed_events,
        'volunteer_attended_events': volunteer_attended_events,
        'active_tab': tab,
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
        messages.info(request, 'You already have a registration for this event and cannot register again.')
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
        messages.success(request, f'Check-in recorded at {timezone.localtime(work_log.check_in_time).strftime("%I:%M %p")}.')
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


@login_required
@require_POST
def checkin_qr(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        body = json.loads(request.body)
        qr_data = body.get('qr_data', '')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'success': False, 'error': 'Invalid request data.'}, status=400)

    # Validate QR code contains this event's unique code
    if not qr_data or event.event_code not in qr_data:
        return JsonResponse({'success': False, 'error': 'This QR code does not belong to this event.'})

    # Look up registration regardless of status to give precise errors
    reg = EventRegistration.objects.filter(volunteer=request.user, event=event).first()
    if not reg:
        return JsonResponse({'success': False, 'error': 'You are not registered for this event.'})
    if reg.status == 'cancelled':
        return JsonResponse({'success': False, 'error': 'Your registration has been cancelled. Please re-register to participate.'})

    work_log, _ = WorkLog.objects.get_or_create(registration=reg)
    if work_log.check_in_time:
        if work_log.check_out_time:
            return JsonResponse({'success': False, 'error': 'You have already checked in and checked out for this event.'})
        return JsonResponse({'success': False, 'error': 'You have already checked in for this event.'})

    work_log.check_in_time = timezone.now()
    work_log.save()
    local_in = timezone.localtime(work_log.check_in_time)
    return JsonResponse({
        'success': True,
        'message': f'Checked in successfully at {local_in.strftime("%I:%M %p")}.',
        'action': 'checkin',
        'check_in_time': local_in.strftime('%I:%M %p'),
    })


@login_required
@require_POST
def checkout_qr(request, pk):
    event = get_object_or_404(Event, pk=pk)
    try:
        body = json.loads(request.body)
        qr_data = body.get('qr_data', '')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'success': False, 'error': 'Invalid request data.'}, status=400)

    # Validate QR code contains this event's unique code
    if not qr_data or event.event_code not in qr_data:
        return JsonResponse({'success': False, 'error': 'This QR code does not belong to this event.'})

    # Look up registration regardless of status so we can give precise errors
    reg = EventRegistration.objects.filter(volunteer=request.user, event=event).first()
    if not reg:
        return JsonResponse({'success': False, 'error': 'You are not registered for this event.'})
    if reg.status == 'cancelled':
        return JsonResponse({'success': False, 'error': 'Your registration has been cancelled.'})

    work_log = WorkLog.objects.filter(registration=reg).first()
    if not work_log or not work_log.check_in_time:
        return JsonResponse({'success': False, 'error': 'You must check in before you can check out.'})
    if work_log.check_out_time:
        return JsonResponse({'success': False, 'error': 'You have already checked out from this event.'})

    work_log.check_out_time = timezone.now()
    delta = work_log.check_out_time - work_log.check_in_time
    work_log.duration_minutes = max(1, int(delta.total_seconds() / 60))
    work_log.save()
    reg.hours_logged = round(work_log.duration_minutes / 60, 2)
    reg.status = 'attended'
    reg.save()
    local_out = timezone.localtime(work_log.check_out_time)
    local_in  = timezone.localtime(work_log.check_in_time)
    return JsonResponse({
        'success': True,
        'message': f'Checked out successfully. Total duration: {work_log.duration_display()}.',
        'action': 'checkout',
        'check_in_time': local_in.strftime('%I:%M %p'),
        'check_out_time': local_out.strftime('%I:%M %p'),
        'duration': work_log.duration_display(),
    })


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




