"""
FILE NAME: urls.py

-------------------------------------------------------------------------------
PART OF PROJECT: SVSU Mentorship Program App

-------------------------------------------------------------------------------
WRITTEN BY:
DATE CREATED:

-------------------------------------------------------------------------------
FILE PURPOSE:
Defines all usable routes for the website.

-------------------------------------------------------------------------------
COMMAND LINE PARAMETER LIST (In Parameter Order):
(NONE)

-------------------------------------------------------------------------------
ENVIRONMENTAL RETURNS:
(NONE)

-------------------------------------------------------------------------------
SAMPLE INVOCATION:
(NONE)

-------------------------------------------------------------------------------
GLOBAL VARIABLE LIST (Alphabetically):
- urlpatterns ([path])

-------------------------------------------------------------------------------
COMPILATION NOTES:

-------------------------------------------------------------------------------
MODIFICATION HISTORY:

WHO     WHEN     WHAT
WJL   3/3/2024   Added file header comment
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mentorship_program_app import views

from .view_routes import navigation
from .view_routes import under_development
from .view_routes import backend_requests
from .view_routes import development as development_views


##All created urls need to go here
urlpatterns = [
    #path('home/', views.home, name='home'),
    #path('login/', views.login, name='login'),
    #path('login/success', views.success, name='success'),  ## some urls dont currently have html to go with them
    
    
    #================NAVIGATION ROUTES================#
    path('', navigation.landing, name='default'),     #Now landing
    # path('landing/', navigation.landing, name='landing'), 
    path('dashboard/', navigation.dashboard, name='dashboard'),
    #=================================================#
    
    #==================LOGICAL ROUTES=================#
    path('landing-post/'                                 , views.landingPost                 , name='landing-post'),
    path('register-test/'                                , under_development.register_mentor , name='register-test'),
    path('register-mentee-test/'                         , under_development.register_mentee , name='register-mentee-test'),
    path('request_mentor/<int:mentee_id>/<int:mentor_id>', backend_requests.request_mentor,name='request mentor'),
   # path('profile_pic/<int:user_id>')
    #8=============================================D~~#

    
    #ADAM + ANDREW + JORDAN TESTING
    path("view_pending", under_development.view_pending_mentors, name="view_pending"),
    path("change_mentor_status", under_development.change_mentor_status, name="change_mentor_status"),
    path("disable-user", under_development.disable_user, name="disable-user"),
    path("enable-user", under_development.enable_user, name="enable-user"),
    path("view_mentor_by_admin", under_development.view_mentor_by_admin, name="view_mentor_by_admin"),
    path("admin_dashboard", navigation.admin_dashboard, name="admin_dashboard"),
    #path("request-mentor", under_development.request_mentor, name="request-mentor"),
    
    # TESTING AND DEV ROUTES WILL NEED TO CHECK/REVIEW BEFORE PUBLISHING FROM LOGAN
    path('role_selection/', views.role_selection, name='role_selection'),
    path('account_activation_mentee/', views.account_activation_mentee, name='account_activation_mentee'),
    path('account_activation_invalid/', views.account_activation_invalid_mentee, name='account_activation_invalid'),
    # CURRENTLY STATIC ROUTE TO VIEW LIST OF MENTORS APPLYING FOR MENTORSHIP ROLE FROM BEN
    path('judgement', views.mentor_judgement, name='mentor_judgement'),
    
    
    path('dashboard/', navigation.dashboard, name='dashboard'),
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
    path('account_activation_mentor/', views.account_activation_mentor, name='account_activation_mentor'),

    path('admin_user_management/', views.admin_user_management, name='admin_user_management'),

    #log in and out routes
    path('login/',views.login_uname_text,name='login'),
    path('logout/',views.logout,name='logout'),

    #development routes
    
    path('dev/show_all_user_roles'           , development_views.display_all_user_roles            ,name='display all user roles'),
    path('dev/profile_pictures'           , development_views.profile_picture_test            ,name='profile_picture_tests'),
    path('dev/generate_random_user_data/' , development_views.generate_random_user_data       ,name='generate_random_user_data'),
    path('dev/populate_default_interests/', development_views.populate_default_interest_values,name='populate_default_interest_values'),
    path('dev/database_test'              , development_views.test_database_setup             ,name='database_test'),
    path('dev/delete_users'               , development_views.delete_users                    ,name='delete users'),
    path('dev/test_login'                 , development_views.test_login_page                 ,name='test login'),
    path('dev/is_logged_in'               , development_views.is_logged_in_test               ,name='logged in test')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

