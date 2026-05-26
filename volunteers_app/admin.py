from django.contrib import admin
from .models import UserProfile, Badge, VolunteerBadge


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_organizer', 'phone', 'total_points', 'availability_weekends')
    list_filter = ('is_organizer', 'availability_weekdays', 'availability_weekends')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_type', 'icon')


@admin.register(VolunteerBadge)
class VolunteerBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    list_filter = ('badge',)
