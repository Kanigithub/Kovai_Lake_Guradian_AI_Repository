"""
URL configuration for clean_lakes_project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('announcements/', views.announcements, name='announcements'),
    path('volunteers/', include('volunteers_app.urls')),
    path('events/', include('events_app.urls')),
    path('lakes/', include('lakes_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
