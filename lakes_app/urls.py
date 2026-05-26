from django.urls import path
from . import views

app_name = 'lakes_app'

urlpatterns = [
    path('', views.lake_list, name='lake_list'),
    path('explore/', views.explore_lakes, name='explore_lakes'),
    path('<int:pk>/', views.lake_detail, name='lake_detail'),
    path('<int:pk>/edit/', views.lake_edit, name='lake_edit'),
    path('<int:pk>/add-photo/', views.lake_add_photo, name='lake_add_photo'),
]
