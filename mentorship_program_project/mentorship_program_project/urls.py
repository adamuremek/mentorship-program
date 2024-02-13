"""
URL configuration for mentorship_program_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from mentorship_program_app import views

urlpatterns = [
    path('', views.default, name='default'),
    path('landing/', views.landing, name='landing'),
    path('landing-post/', views.landingPost, name='landing-post'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile-card/', views.profileCard, name='profile-card'),

    # TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING
    path('role_selection/', views.role_selection, name='role_selection'),

    path('account_activation_mentee/', views.account_activation_mentee, name='account_activation_mentee'),
    path('account_activation_mentee_invalid/', views.account_activation_invalid_mentee, name='account_activation_invalid_mentee'),
    path('account_activation_mentee_valid/', views.account_activation_valid_mentee, name='account_activation_valid_mentee'),
    path('account_creation_1_mentee/', views.account_creation_1_mentee, name='account_creation_1_mentee'),
    path('account_creation_2_mentee/', views.account_creation_2_mentee, name='account_creation_2_mentee'),
    path('account_creation_3_mentee/', views.account_creation_3_mentee, name='account_creation_3_mentee'),

    path('account_activation_mentor/', views.account_activation_mentor, name='account_activation_mentor'),
    path('account_creation_0_mentor/', views.account_creation_0_mentor, name='account_creation_0_mentor'),
    path('account_creation_1_mentor/', views.account_creation_1_mentor, name='account_creation_1_mentor'),
    path('account_creation_2_mentor/', views.account_creation_2_mentor, name='account_creation_2_mentor'),

    path('admin/', admin.site.urls),
]
