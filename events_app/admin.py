from django.contrib import admin
from .models import Event, EventRole, EventRegistration


class EventRoleInline(admin.TabularInline):
    model = EventRole
    extra = 1


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registered_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'location', 'status', 'registered_count', 'max_volunteers')
    list_filter = ('status', 'date', 'lake')
    search_fields = ('title', 'location', 'description')
    inlines = [EventRoleInline, EventRegistrationInline]
    date_hierarchy = 'date'


@admin.register(EventRole)
class EventRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'max_volunteers')
    list_filter = ('event',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'event', 'role', 'status', 'hours_logged', 'registered_at')
    list_filter = ('status', 'event')
    search_fields = ('volunteer__username', 'event__title')
