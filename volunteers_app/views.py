from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UserProfile, VolunteerBadge
from .forms import VolunteerRegistrationForm, UserProfileForm, NGORegistrationForm
from events_app.models import EventRegistration


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    individual_form = VolunteerRegistrationForm()
    ngo_form = NGORegistrationForm()
    active_tab = 'individual'

    if request.method == 'POST':
        reg_type = request.POST.get('reg_type', 'individual')
        if reg_type == 'ngo':
            active_tab = 'ngo'
            ngo_form = NGORegistrationForm(request.POST)
            if ngo_form.is_valid():
                user = ngo_form.save()
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.account_type = 'ngo'
                profile.organization_name = ngo_form.cleaned_data.get('organization_name', '')
                profile.organization_type = ngo_form.cleaned_data.get('organization_type', '')
                profile.organization_size = ngo_form.cleaned_data.get('organization_size')
                profile.organization_website = ngo_form.cleaned_data.get('organization_website', '')
                profile.organization_description = ngo_form.cleaned_data.get('organization_description', '')
                profile.save()
                messages.success(request, f'NGO account for "{profile.organization_name}" created! Please log in.')
                return redirect('volunteers_app:login')
        else:
            active_tab = 'individual'
            individual_form = VolunteerRegistrationForm(request.POST)
            if individual_form.is_valid():
                user = individual_form.save()
                UserProfile.objects.get_or_create(user=user)
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('volunteers_app:login')

    return render(request, 'volunteers_app/register.html', {
        'form': individual_form,
        'ngo_form': ngo_form,
        'active_tab': active_tab,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'volunteers_app/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('volunteers_app:login')


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    registrations = EventRegistration.objects.filter(
        volunteer=request.user
    ).select_related('event').order_by('-registered_at')
    badges = VolunteerBadge.objects.filter(user=request.user).select_related('badge')
    total_hours = profile_obj.total_hours()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('volunteers_app:profile')
    else:
        form = UserProfileForm(instance=profile_obj)

    context = {
        'profile': profile_obj,
        'form': form,
        'registrations': registrations,
        'badges': badges,
        'total_hours': total_hours,
    }
    return render(request, 'volunteers_app/profile.html', context)


@login_required
def leaderboard(request):
    profiles = UserProfile.objects.select_related('user').order_by('-total_points')[:20]
    return render(request, 'volunteers_app/leaderboard.html', {'profiles': profiles})
