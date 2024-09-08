from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('announcement/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    # Add other paths here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

