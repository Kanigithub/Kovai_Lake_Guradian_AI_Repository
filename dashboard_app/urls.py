from django.urls import path
from . import views

app_name = 'dashboard_app'

urlpatterns = [
    # Dashboard home
    path('', views.organizer_dashboard, name='organizer_dashboard'),

    # Volunteer management
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('volunteers/<int:user_id>/', views.volunteer_detail, name='volunteer_detail'),
    path('volunteers/<int:user_id>/toggle-organizer/', views.toggle_organizer, name='toggle_organizer'),
    path('volunteers/<int:user_id>/award-badge/', views.award_badge, name='award_badge'),
    path('badges/', views.manage_badges, name='manage_badges'),
    path('badges/create/', views.create_badge, name='create_badge'),
    path('badges/<int:badge_id>/delete/', views.delete_badge, name='delete_badge'),

    # Event management
    path('events/', views.manage_events, name='manage_events'),
    path('events/<int:event_id>/registrations/', views.manage_registrations, name='manage_registrations'),
    path('events/<int:event_id>/status/', views.update_event_status, name='update_event_status'),
    path('registrations/<int:reg_id>/update/', views.update_registration, name='update_registration'),

    # Lake management
    path('lakes/', views.manage_lakes, name='manage_lakes'),

    # Announcement management
    path('announcements/', views.manage_announcements, name='manage_announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:ann_id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcements/<int:ann_id>/delete/', views.delete_announcement, name='delete_announcement'),

    # Message management
    path('messages/', views.manage_messages, name='manage_messages'),
    path('messages/send/', views.send_message, name='send_message'),

    # Import volunteers
    path('import-volunteers/', views.import_volunteers, name='import_volunteers'),
    path('import-volunteers/template/', views.download_volunteer_template, name='download_volunteer_template'),

    # AI Lake Scan
    path('scan-lake/', views.scan_lake_page, name='scan_lake_page'),
    path('api/scan-lake/', views.scan_lake, name='scan_lake'),
]
