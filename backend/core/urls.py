from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/create/', views.meeting_create, name='meeting_create'),
    path('meetings/<int:pk>/edit/', views.meeting_edit, name='meeting_edit'),
    path('meetings/<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
    path('participants/', views.participant_list, name='participant_list'),
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/edit/', views.participant_edit, name='participant_edit'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('recordings/', views.recording_list, name='recording_list'),
    path('recordings/create/', views.recording_create, name='recording_create'),
    path('recordings/<int:pk>/edit/', views.recording_edit, name='recording_edit'),
    path('recordings/<int:pk>/delete/', views.recording_delete, name='recording_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
