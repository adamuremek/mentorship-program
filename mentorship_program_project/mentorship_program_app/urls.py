from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mentorship_program_app import views



##All created urls need to go here
urlpatterns = [
    #path('home/', views.home, name='home'),
    #path('login/', views.login, name='login'),
    #path('login/success', views.success, name='success'),  ## some urls dont currently have html to go with them

    path('', views.default, name='default'),
    path('landing/', views.landing, name='landing'),

    # TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING FROM LOGAN
    path('role_selection/', views.role_selection, name='role_selection'),
    path('account_activation_mentee/', views.account_activation_mentee, name='account_activation_mentee'),
    path('account_activation_invalid/', views.account_activation_invalid_mentee, name='account_activation_invalid'),
    path('', views.default, name='default'),
    path('landing/', views.landing, name='landing'),
    path('landing-post/', views.landingPost, name='landing-post'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('faq/', views.faq, name='faq'),
    path('profile-card/', views.profileCard, name='profile-card'),
    
    path('register/mentee/', views.register_mentee, name='register_mentee'),
    path('register/mentor/', views.register_mentor, name='register_mentor'),
    path('thebigmove/', views.THEBIGMOVE, name='thebigmove'),

    # TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING
    path('role_selection/', views.role_selection, name='role_selection'),

    path('account_activation_mentee/', views.account_activation_mentee, name='account_activation_mentee'),
    path('account_activation_mentee_invalid/', views.account_activation_invalid_mentee, name='account_activation_invalid_mentee'),
    path('account_activation_mentee_valid/', views.account_activation_valid_mentee, name='account_activation_valid_mentee'),
    path('account_creation_1_mentee/', views.account_creation_1_mentee, name='account_creation_1_mentee'),
    path('account_creation_2_mentee/', views.account_creation_2_mentee, name='account_creation_2_mentee'),
    path('account_activation_mentor/', views.account_activation_mentor, name='account_activation_mentor'),

    #log in and out routes
    path('login/',views.login_uname_text,name='login'),
    path('logout/',views.logout,name='logout'),

    #development routes
    path('dev/profile_pictures',views.profile_picture_test,name='profile_picture_tests'),
    path('dev/generate_random_user_data/',views.generate_random_user_data,name='generate_random_user_data'),
    path('dev/populate_default_interests/',views.populate_default_interest_values,name='populate_default_interest_values'),
    path('dev/database_test',views.test_database_setup,name='database_test'),
    path('dev/delete_users',views.delete_users,name='delete users'),
    path('dev/test_login',views.test_login_page,name='test login'),
    path('dev/is_logged_in',views.is_logged_in_test,name='logged in test')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

