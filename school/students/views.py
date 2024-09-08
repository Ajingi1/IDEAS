from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Enrollment
from news.models import News, Announcement  # Import your News and Announcement models

# Create your views here.

def index(request):
    latest_news = News.objects.all().order_by('-time')[:4]  # Get the latest 3 news
    latest_announcements = Announcement.objects.all().order_by('-time')[:4]  # Get the latest 3 announcements

    context = {
        'latest_news': latest_news,
        'latest_announcements': latest_announcements,
    }
    return render(request, 'index.html', context)

# render news
def news_detail(request, news_id):
    # Get the specific news item
    news_item = get_object_or_404(News, id=news_id)
    
    # Get the latest news items, excluding the current news item
    latest_news = News.objects.exclude(id=news_id).order_by('-time')[:4]

    
    # Process content of the current news item to split into paragraphs
    paragraphs = [para.strip() + '.' for para in news_item.content.split('.') if para.strip()]

    context = {
        'latest_news': latest_news,
        'paragraphs': paragraphs,
        'news': news_item,
        # 'latest_announcements': latest_announcements,
    }
    return render(request, 'news_detail.html', context )

# render announcements
def announcement_detail(request, announcement_id):
    # Get the specific anouncement item
    announcement_item = get_object_or_404(Announcement, id=announcement_id)
    
    # Get latest announcements
    latest_announcements = Announcement.objects.all().order_by('-time')[:3]  # Get the latest 3 announcements
    
    # Process content of the current announcement item to split into paragraphs
    paragraphs = [para.strip() + '.' for para in announcement_item.content.split('.') if para.strip()]
    
    context = {
        'paragraphs': paragraphs,
        'announcement': announcement_item,
        'latest_announcements': latest_announcements,
    }
    return render(request, 'announcements_detail.html', context )
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to a home page or another page after successful login
        else:
            # Handle the case where authentication fails
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error': error_message})
    else:
        return render(request, 'login.html')
@login_required
def logout(request):
    """Logs out the user and redirects to the home page."""
    auth_logout(request)
    return redirect('index')  # Redirect to a view named 'index'
    
@login_required
def dashboard(request):
    # Assuming the user is logged in and has a related student profile
    student = get_object_or_404(Student, user=request.user)
    # Get all enrollments for the student
    # enrollments = Enrollment.objects.filter(student=student)

    # If you want to ensure that there are enrollments or raise a 404 if none exist:
    enrollments = get_list_or_404(Enrollment, student=student)
        
    context = {
        'student': student,
        'enrollments': enrollments
    }
    # Pass the student and enrolled objects to the template context
    return render(request, 'dashboard.html', context)


# For now there is no need for this page bacause only admin can regisrter students or teacher
def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')


@login_required
def profile(request):
    #Assuming the user is logged in and has a related student profile
    student = get_object_or_404(Student, user=request.user)
    
    context = {
        'student': student,
    }
    return render(request, 'profile.html', context)


@login_required
def courses(request):
    pass