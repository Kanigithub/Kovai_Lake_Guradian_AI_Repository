from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lake, LakePhoto
from .forms import LakeForm, LakePhotoForm


def lake_list(request):
    lakes = Lake.objects.prefetch_related('photos').all()
    return render(request, 'lakes_app/lake_list.html', {'lakes': lakes})


def explore_lakes(request):
    lakes = Lake.objects.prefetch_related('photos').all()
    return render(request, 'lakes_app/explore_lakes.html', {'lakes': lakes})


def lake_detail(request, pk):
    lake = get_object_or_404(Lake, pk=pk)
    before_photos = lake.photos.filter(photo_type='before')
    after_photos = lake.photos.filter(photo_type='after')
    general_photos = lake.photos.filter(photo_type='general')
    events = lake.events.filter(status='upcoming').order_by('date')[:5]
    return render(request, 'lakes_app/lake_detail.html', {
        'lake': lake,
        'before_photos': before_photos,
        'after_photos': after_photos,
        'general_photos': general_photos,
        'events': events,
    })


@login_required
def lake_edit(request, pk):
    lake = get_object_or_404(Lake, pk=pk)
    if not request.user.userprofile.is_organizer:
        messages.error(request, 'Only organizers can edit lake information.')
        return redirect('lakes_app:lake_detail', pk=pk)
    if request.method == 'POST':
        form = LakeForm(request.POST, instance=lake)
        if form.is_valid():
            form.save()
            messages.success(request, f'Lake "{lake.name}" updated successfully.')
            return redirect('lakes_app:lake_detail', pk=pk)
    else:
        form = LakeForm(instance=lake)
    return render(request, 'lakes_app/lake_edit.html', {'form': form, 'lake': lake})


@login_required
def lake_add_photo(request, pk):
    lake = get_object_or_404(Lake, pk=pk)
    if not request.user.userprofile.is_organizer:
        messages.error(request, 'Only organizers can add photos.')
        return redirect('lakes_app:lake_detail', pk=pk)
    if request.method == 'POST':
        form = LakePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.lake = lake
            photo.save()
            messages.success(request, 'Photo added successfully.')
            return redirect('lakes_app:lake_detail', pk=pk)
    else:
        form = LakePhotoForm()
    return render(request, 'lakes_app/lake_add_photo.html', {'form': form, 'lake': lake})
