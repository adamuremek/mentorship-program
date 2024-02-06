from django.urls import path
from . import views



##All created urls need ot go here
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('login/success', views.success, name='success'),  ## some urls dont currently have html to go with them

    path('', views.default, name='default'),
    path('landing/', views.landing, name='landing'),

    # TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING FROM LOGAN
    path('role_selection/', views.role_selection, name='role_selection'),
    path('account_activation_mentee/', views.account_activation_mentee, name='account_activation_mentee'),
    path('account_activation_invalid/', views.account_activation_invalid_mentee, name='account_activation_invalid'),

]