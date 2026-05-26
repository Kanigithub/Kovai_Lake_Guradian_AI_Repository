from django.urls import path
from . import views

app_name = 'events_app'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('<int:pk>/register/', views.event_register, name='event_register'),
    path('<int:pk>/cancel/', views.event_cancel, name='event_cancel'),
    path('checkin/<int:pk>/', views.check_in, name='check_in'),
    path('checkout/<int:pk>/', views.check_out, name='check_out'),
]
