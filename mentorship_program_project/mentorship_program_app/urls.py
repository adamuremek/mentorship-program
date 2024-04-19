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
Adam U. 4/15     organized this whole page
"""

from django.urls import include,path, re_path

from django.conf import settings
from django.conf.urls.static import static

from .routes import register_routes, profiles_routes, mentorship_routes, user_management_routes, account_routes, login_routes
from .routes import password_routes, pending_mentor_routes, dashboard_routes, reporting, interests_routes, notes_routes, landing_routes
from .routes import user_reports_routes, admin_file_management_routes, settings_routes, misc_routes, faq_routes, verify_mentee_undergrad_routes
from .routes import mentor_mfa

##All created urls need to go here
urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    
        #Profile Routes
        path("save_profile_info/<int:user_id>", profiles_routes.save_profile_info, name="save_profile_info"),
        path("universal_profile/<int:user_id>", profiles_routes.universalProfile, name="universal_profile"),

        #Registration Routes
        path('register-mentee-test/', register_routes.register_mentee_render , name='register-mentee-test'),
        path('register-mentor-form/', register_routes.register_mentor_submit , name='register-mentor-form'),
        path('register/mentee/', register_routes.register_mentee_render, name='register_mentee'),
        path('register/mentor/', register_routes.register_mentor_submit, name='register_mentor'),
        
        #Login Routes
        path('login/',login_routes.login_uname_text,name='login'),
        path('logout/',login_routes.logout,name='logout'),
        path('saml/login', login_routes.saml_login, name='saml_login'),

        #Multi-factor Authentication
        path('mentor/2fa/', mentor_mfa.mentor_otp_request,name='passcode_request'),
        path('mentor/2fa/otp', mentor_mfa.mentor_otp_validate,name='passcode_validation'),
        path('valid', login_routes.complete_login,name="complete_login"),

        #Landing Routes
        path('landing-post/', landing_routes.landingPost, name='landing-post'),
        path('', landing_routes.landing, name='default'),

        #Mentorship Routes
        path('request_mentor/<int:mentee_id>/<int:mentor_id>', mentorship_routes.request_mentor,name='request mentor'),
        path('assign_mentee/<int:mentee_account_id>/<int:mentor_account_id>', mentorship_routes.create_mentorship, name='assign mentee to mentor'),
        path("accept_mentorship_request/<int:mentee_user_account_id>/<int:mentor_user_account_id>",mentorship_routes.accept_mentorship_request,name="accept_mentorship_request"),
        path("reject_mentorship_request/<int:mentee_user_account_id>/<int:mentor_user_account_id>", mentorship_routes.reject_mentorship_request, name="reject_mentorship_request"),
        path('create_mentorship/<int:mentee_user_account_id>/<int:mentor_user_account_id>', mentorship_routes.create_mentorship, name='add mentorship'),
        path("delete_mentorship/<int:mentee_user_account_id>", mentorship_routes.delete_mentorship, name="delete_mentorship"),

        #User Management Routes
        path('create_new_orgnization/<str:org_name>', user_management_routes.admin_create_new_org, name='create new organization'),
        path('delete_orgnization/<int:org_id>', user_management_routes.admin_delete_org, name='delete organization'), 
        path('edit_mentor_organization/<int:mentor_id>/<int:org_id>', user_management_routes.edit_mentors_org, name='edit mentor organization'),
        path('remove_mentors_org/<int:mentor_id>/<int:org_id>', user_management_routes.remove_mentors_org, name='remove mentor organization'),
        path('promote_organization_admin/<int:promoted_mentor_id>', user_management_routes.promote_org_admin, name='prmote mentor to organization admin'),
        path('get_next_organization_id', user_management_routes.get_next_org, name='get last organziation id'),
        path("promote_org_admin/<int:promoted_mentor_id>", user_management_routes.promote_org_admin, name="promote_org_admin"),
        path('admin_user_management/', user_management_routes.admin_user_management, name='admin_user_management'),

        #Account Routes
        path('disable_user', account_routes.disable_user, name='disable user'),
        path('enable_user', account_routes.enable_user, name='enable user'),
        path("deactivate_your_own_account", account_routes.deactivate_your_own_account, name="deactivate_your_own_account"),

        #Password Routes
        path("reset_request", password_routes.reset_request, name="reset_request"),
        path("reset_password", password_routes.reset_password, name="reset_password"),
        re_path(r'^request_reset_page(?:/(?P<token>\w{30}))?/$', password_routes.request_reset_page, name="request_reset_page"),
        path('check_email_for_password_reset', password_routes.check_email_for_password_reset, name='check_email_for_password_reset'),
        path('check-email', password_routes.check_email, name='check_email'),
        path("change_password", password_routes.change_password, name="change_password"),
    
        #Pending Mentor Routes
        path("view_pending", pending_mentor_routes.view_pending_mentors, name="view_pending"),
        path("change_mentor_status", pending_mentor_routes.change_mentor_status, name="change_mentor_status"),
        path("view_mentor_by_admin", pending_mentor_routes.view_mentor_by_admin, name="view_mentor_by_admin"),

        #Dashboard Routes
        path("admin_dashboard", dashboard_routes.admin_dashboard, name="admin_dashboard"),
        path('dashboard/', dashboard_routes.dashboard, name='dashboard'),

        #Reporting Rotes
        path("generate_report", reporting.generate_report, name="generate_report"),

        #Interests Routes
        path("update_interests", interests_routes.update_interests, name="update_interests"),

        #Notes Routes
        path("create_note", notes_routes.create_note, name="create_note"),
        path("update_note", notes_routes.update_note, name="update_note"),
        path("remove_note", notes_routes.remove_note, name="remove_note"),

        #User Reports Routes
        path("resolve_report", user_reports_routes.resolve_report, name="resolve_report"),
        path('admin_reported_users/', user_reports_routes.admin_reported_users, name='admin_reported_users'),
        path('report_user/', user_reports_routes.report_user, name='report_user'),
        
        #Admin File Management Routes
        path("available_mentees", admin_file_management_routes.available_mentees, name="available_mentees"),
        path("process_file", admin_file_management_routes.process_file, name="process_file"),
        path("add_remove_mentees_from_file", admin_file_management_routes.add_remove_mentees_from_file, name="add_remove_mentees_from_file"),
    
        #Settings Routes
        path("toggle_notifications/<status>", settings_routes.toggle_notifications, name="toggle_notifications"),
        path('settings', settings_routes.change_settings, name='change_settings'),

        #FAQ Routes
        path('faq/', faq_routes.faq, name='faq'),

        #Verify Mentee Undergrad Routes
        path("verify-mentee-ug-status/", verify_mentee_undergrad_routes.verify_mentee_ug_status, name='verify_mentee_ug_status'),

        #Misc Routes
        path('role_selection/', misc_routes.role_selection, name='role_selection'),
        path('account_activation_mentee/', misc_routes.account_activation_mentee, name='account_activation_mentee'),
        path('account_activation_invalid/', misc_routes.account_activation_invalid_mentee, name='account_activation_invalid'),
        path('account_activation_mentee_invalid/', misc_routes.account_activation_invalid_mentee, name='account_activation_invalid_mentee'),
        path('account_activation_mentee_valid/', misc_routes.account_activation_valid_mentee, name='account_activation_valid_mentee'),
        path('account_activation_mentor/', misc_routes.account_activation_mentor, name='account_activation_mentor'),
        path('profile-card/', misc_routes.profileCard, name='profile-card'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

