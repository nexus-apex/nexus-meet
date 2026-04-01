import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Meeting, Participant, Recording


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['meeting_count'] = Meeting.objects.count()
    ctx['meeting_scheduled'] = Meeting.objects.filter(status='scheduled').count()
    ctx['meeting_live'] = Meeting.objects.filter(status='live').count()
    ctx['meeting_completed'] = Meeting.objects.filter(status='completed').count()
    ctx['participant_count'] = Participant.objects.count()
    ctx['participant_host'] = Participant.objects.filter(role='host').count()
    ctx['participant_co_host'] = Participant.objects.filter(role='co_host').count()
    ctx['participant_presenter'] = Participant.objects.filter(role='presenter').count()
    ctx['recording_count'] = Recording.objects.count()
    ctx['recording_processing'] = Recording.objects.filter(status='processing').count()
    ctx['recording_ready'] = Recording.objects.filter(status='ready').count()
    ctx['recording_expired'] = Recording.objects.filter(status='expired').count()
    ctx['recording_total_size_mb'] = Recording.objects.aggregate(t=Sum('size_mb'))['t'] or 0
    ctx['recent'] = Meeting.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def meeting_list(request):
    qs = Meeting.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'meeting_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def meeting_create(request):
    if request.method == 'POST':
        obj = Meeting()
        obj.title = request.POST.get('title', '')
        obj.host = request.POST.get('host', '')
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.status = request.POST.get('status', '')
        obj.participants = request.POST.get('participants') or 0
        obj.meeting_url = request.POST.get('meeting_url', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/meetings/')
    return render(request, 'meeting_form.html', {'editing': False})


@login_required
def meeting_edit(request, pk):
    obj = get_object_or_404(Meeting, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.host = request.POST.get('host', '')
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.status = request.POST.get('status', '')
        obj.participants = request.POST.get('participants') or 0
        obj.meeting_url = request.POST.get('meeting_url', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/meetings/')
    return render(request, 'meeting_form.html', {'record': obj, 'editing': True})


@login_required
def meeting_delete(request, pk):
    obj = get_object_or_404(Meeting, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/meetings/')


@login_required
def participant_list(request):
    qs = Participant.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(role=status_filter)
    return render(request, 'participant_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def participant_create(request):
    if request.method == 'POST':
        obj = Participant()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.meeting_title = request.POST.get('meeting_title', '')
        obj.role = request.POST.get('role', '')
        obj.joined = request.POST.get('joined') == 'on'
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.save()
        return redirect('/participants/')
    return render(request, 'participant_form.html', {'editing': False})


@login_required
def participant_edit(request, pk):
    obj = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.meeting_title = request.POST.get('meeting_title', '')
        obj.role = request.POST.get('role', '')
        obj.joined = request.POST.get('joined') == 'on'
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.save()
        return redirect('/participants/')
    return render(request, 'participant_form.html', {'record': obj, 'editing': True})


@login_required
def participant_delete(request, pk):
    obj = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/participants/')


@login_required
def recording_list(request):
    qs = Recording.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'recording_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def recording_create(request):
    if request.method == 'POST':
        obj = Recording()
        obj.title = request.POST.get('title', '')
        obj.meeting_title = request.POST.get('meeting_title', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.date = request.POST.get('date') or None
        obj.status = request.POST.get('status', '')
        obj.download_url = request.POST.get('download_url', '')
        obj.save()
        return redirect('/recordings/')
    return render(request, 'recording_form.html', {'editing': False})


@login_required
def recording_edit(request, pk):
    obj = get_object_or_404(Recording, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.meeting_title = request.POST.get('meeting_title', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.size_mb = request.POST.get('size_mb') or 0
        obj.date = request.POST.get('date') or None
        obj.status = request.POST.get('status', '')
        obj.download_url = request.POST.get('download_url', '')
        obj.save()
        return redirect('/recordings/')
    return render(request, 'recording_form.html', {'record': obj, 'editing': True})


@login_required
def recording_delete(request, pk):
    obj = get_object_or_404(Recording, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/recordings/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['meeting_count'] = Meeting.objects.count()
    data['participant_count'] = Participant.objects.count()
    data['recording_count'] = Recording.objects.count()
    return JsonResponse(data)
