from django.contrib import admin
from .models import Event, EventRole, EventRegistration, WorkLog


class EventRoleInline(admin.TabularInline):
    model = EventRole
    extra = 1


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registered_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'lake', 'date', 'status', 'max_volunteers')
    list_filter = ('status', 'lake')
    search_fields = ('title', 'location')
    inlines = [EventRoleInline, EventRegistrationInline]


@admin.register(EventRole)
class EventRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_volunteers')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'role', 'status', 'hours_logged', 'registered_at')
    list_filter = ('status', 'event')


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('registration', 'check_in_time', 'check_out_time', 'duration_minutes')
