from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor_registration/', views.doctor_registration, name='doctor_registration'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('patient_profile/', views.patient_profile, name='patient_profile'),
    path('health_analysis/', views.analyze_health_data, name='health_analysis'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)