
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from mentorship_program_app.models import *
from .status_codes import bad_request_400
from utils.development import print_debug
from .emails import *
from django.http import JsonResponse
from ..models import *
from django.db.models import *
def edit_mentors_org(req : HttpRequest, mentor_id: int, org_id : int):
    '''
    Description
    -----------
    Function to assign a new organization to a mentor. This operation can only be performed by a super admin. It updates the organization associated with a specified mentor to a new organization based on the provided organization ID.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the session of the currently logged-in user. Used to check if the user has super admin privileges.
    - mentor_id : int
        The ID of the mentor whose organization affiliation is to be edited.
    - org_id : int
        The ID of the new organization to which the mentor will be assigned.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome of the operation. If successful, it confirms that the organization was updated. If the operation fails due to lack of permissions, it returns a 400 Bad Request response.

    Authors
    -------
    - Andrew P.
    '''
    user_from_session = User.from_session(req.session)
    if not user_from_session.is_super_admin():
        return bad_request_400("Permission denied")
    
    mentor_account = Mentor.objects.get(id=mentor_id)
    
    old_org = User.objects.get(id=mentor_account.account_id).get_organization()
    new_org = Organization.objects.get(id=org_id)
    mentor_account.organization.set([new_org])
    SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_ORGANIZATION_CHANGED_EVENT, str_details=f'Handled by: {user_from_session.id},  {new_org.str_org_name} -> {old_org}')
    # mentor_account.organization.remove(new_org)

    return HttpResponse("Organization updated")

def remove_mentors_org(req : HttpRequest, mentor_id: int, org_id : int):
    '''
    Description
    -----------
    Function to remove a organization from a mentor. This operation can be performed by organization admins. It updates the organization associated with a specified mentor to remove the mentor based on the provided mentor ID.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the session of the currently logged-in user. Used to check if the user has organization admin privileges.
    - mentor_id : int
        The ID of the mentor whose organization affiliation is to be edited.
    - org_id : int
        The ID of the new organization to which the mentor will be removed.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome of the operation. If successful, it confirms that the organization was updated. If the operation fails due to lack of permissions, it returns a 400 Bad Request response.

    Authors
    -------
    - Anthony P.
    '''
    user_from_session = User.from_session(req.session)
    if not (user_from_session.is_an_org_admin() or user_from_session.is_super_admin()) :
        return bad_request_400("Permission denied")

    mentor_account = Mentor.objects.get(id=mentor_id)
    new_org = Organization.objects.get(id=org_id)
    mentor_account.organization.remove(new_org)

    return HttpResponse("Organization updated")

def promote_org_admin(req : HttpRequest, promoted_mentor_id : int):
    '''
    Description
    -----------
    Function to promote a new mentor to the position of organization admin. This action can be performed by a super admin or the current organization admin. It updates the designated organization's admin to the newly promoted mentor.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object, which should carry the session of the currently logged-in user.
    - promoted_mentor_id : int
        The ID of the mentor who is to be promoted to the organization admin.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome. If the operation is successful, it returns a confirmation message. If the operation fails due to permission issues, it returns a 400 Bad Request response.

    Authors
    -------
    - Andrew P.
    - Adam U.
    '''

    # gets the user from the session to check if theyre a super admin
    user_from_session = User.from_session(req.session)
    is_org_admin = False
    
    # if user is not super admin, check if they're the org admin for the org being changed
    if not user_from_session.is_super_admin():
        mentor_account = Mentor.objects.get(account=user_from_session.id)
        current_org_admin = Organization.objects.get(mentor=mentor_account).admin_mentor
        is_org_admin = current_org_admin.id == mentor_account.id
        print("org")
    else:
        print("super admin")
        
    if not user_from_session.is_super_admin() and not is_org_admin:
        return bad_request_400("Permission denied")
    
    # promote them to super admin
    new_org_admin= Mentor.objects.get(id=promoted_mentor_id)
    org = Organization.objects.get(mentor=new_org_admin)
    org.admin_mentor = new_org_admin
    org.save()

    return HttpResponse("Org Admin updated")

def admin_delete_org(req: HttpRequest, org_id: int):
    '''
    Description
    -----------
    Function to delete an existing organization. This operation is restricted to super admins only, ensuring that only authorized users can remove organizations from the system. It deletes the organization corresponding to the provided organization ID.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the session of the currently logged-in user. Used to verify if the user possesses super admin privileges.
    - org_id : int
        The unique identifier of the organization to be deleted.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome of the operation. If successful, it confirms that the organization was deleted. If the operation fails due to lack of permissions or if the specified organization does not exist, it returns a 400 Bad Request response.

    Authors
    -------
    - Andrew P.
    '''
    user_from_session = User.from_session(req.session)
    if not user_from_session.is_super_admin():
        return bad_request_400("Permission denied")
    org = Organization.objects.get(id=org_id)
    SystemLogs.objects.create(str_event=SystemLogs.Event.ORGANIZATION_DELETED_EVENT, str_details=f'Handled by: {user_from_session.id}, Deleted: {org.str_org_name}')
    org.delete()
    return HttpResponse("Organization deleted")

def get_next_org(req: HttpRequest):
    '''
    Description
    -----------
    Function creates a tempary placehold organization stores the id, then deletes it, returns the string value of the next created organization object. This operation is restricted to super admins only, ensuring that only authorized users can see organization records from the system.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the session of the currently logged-in user. Used to verify if the user possesses super admin privileges.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome of the operation. If successful, it confirms that the organization was deleted. If the operation fails due to lack of permissions or if the specified organization does not exist, it returns a 400 Bad Request response.

    Authors
    -------
    - Anthony P.
    '''
    user_from_session = User.from_session(req.session)
    if not user_from_session.is_super_admin():
        return bad_request_400("Permission denied")
    
    temp_org = Organization.objects.create(str_org_name="PLACEHOLDER")
    organization_id = str(temp_org)
    temp_org.delete()

    return JsonResponse({'organization_id': organization_id})

def admin_create_new_org(req : HttpRequest, org_name : str):
    '''
    Description
    -----------
    Function to create a new organization. This action is restricted to super admins only. It creates an organization with the given name.

    Parameters
    ----------
    - req : HttpRequest
        The HTTP request object containing the session of the currently logged-in user. This is used to verify if the user has super admin privileges.
    - org_name : str
        The name of the new organization to be created.

    Returns
    -------
    HttpResponse
        Returns an HTTP response indicating the outcome of the operation. If the operation is successful, it confirms that the organization was created. If the operation fails due to lack of permissions, it returns a 400 Bad Request response.

    Authors
    -------
    - Andrew P.
    '''
    user_from_session = User.from_session(req.session)
    if not user_from_session.is_super_admin():
        return bad_request_400("Permission denied")
    org = Organization.objects.create(str_org_name=org_name)
    SystemLogs.objects.create(str_event=SystemLogs.Event.ORGANIZATION_CREATED_EVENT, str_details=f'Handled by: {user_from_session.id}, Added: {org.str_org_name}')
    return HttpResponse("Organization created")


def admin_user_management(request):
    '''
    Modified: 04/06/2024 Tanner K.
    -   Added functionality for org admins to access page. Primary change is organization 
        creation is directly tied to the boolean bl_user_org_admin and an if/elif block. 
    Modified: 2024/04/18 Justin Goupil
    -   mentor_list in organizations.append( . . . ) no longer appends MENTOR_PENDING
    '''
    
    template = loader.get_template('admin/user_management.html')
    session_user = User.from_session(request.session)

    # Create storge for list
    organizations = []
    mentees = []

    # Create var for checking if user is org admin
    bl_user_org_admin = False

    # Load from database based on role
    # Check if user is an admin
    if (session_user.is_super_admin()):
        print_debug("loading with role admin")
        # Get all mentee, mentor, and organization data from database
        user_management_mentee_data = Mentee.objects
        user_management_mentor_data = Mentor.objects.filter(account__str_role=User.Role.MENTOR)
        user_management_organizations_data = Organization.objects

        orgs = user_management_organizations_data.select_related(
                                            "admin_mentor"
                                ).prefetch_related(
                                                    "mentor_set",
                                                    "mentor_set___mentee_set",
                                                    "mentor_set__account",
                                                    "mentor_set___mentee_set__account",
                                                    "mentor_set__administered_organizations"
                                                    ).filter(mentor__account__str_role=User.Role.MENTOR)

    # Check if user is an organization admin
    elif (session_user.is_an_org_admin()):
        print_debug("hello from the organization admin side of things UwU")
        # TODO NEED TO SET UP TO GET ONLY DATA THAT IS NEEDED FOR THAT ORG, ONLY MENTORS WITHIN ORG AND METEES REALTED TO THEM
        # MAYBE FILTER MENTORS BY ORG AND METEES BY MENTORS WITHIN ORG
        
        bl_user_org_admin = True

        # Get all mentee data, only the admin's organization, and mentor data from within the organization
        # user_management_mentee_data = Mentee.objects
        # user_management_mentor_data = Mentor.objects

        #TODO: you can be admin of more than one organization so get will error since it expects a single return value,
        #this should be a filter instead of a git, ill chage it if I get to it in time with optimization, but ima leave this note
        #here for others or incase I forget -dk
        organization = Organization.objects.get(admin_mentor_id=session_user.mentor)
        user_management_mentee_data = Mentee.objects.filter(mentor__organization=organization)
        user_management_mentor_data = Mentor.objects.filter(organization=organization)

        user_management_organizations_data = organization

        orgs = [organization]

        # return HttpResponse(organization, mentees_with_mentors_in_organization)

    else:
        return HttpResponseRedirect("/dashboard")


    # Cycle through organizations
    for organization in orgs:
        # Inizilize empty list for mentors and admins
        org_admin = None
        mentor_list = []
        
        if organization.admin_mentor != None:
            org_admin = get_mentor_data_from_mentor(organization.admin_mentor,session_user)

        #get_mentor_data_from_mentor(m,session_user) 
        for m in organization.mentor_set.all(): 
            m = get_mentor_data_from_mentor(m,session_user)
            #print(m['account'].account.str_role)

            if m['account'].account.str_role==User.Role.MENTOR:
                if org_admin != None:
                    if organization.admin_mentor.id != m['account'].id:
                        #User is not the organization admin.
                        mentor_list.append(m)
                else:
                    #No organization admin exists yet.
                    mentor_list.append(m)
            #else
                #Not a approved mentor.
        
        organizations.append(
            {
                'organization': organization,
                'id': str(organization),
                'name': organization.str_org_name,
                'admin_list': [org_admin] if org_admin != None else [], #this def does not need to be a list now
                                                                        #unless we want to re-listify admins which we could do
                'mentor_list':  mentor_list
            }
        )

    #TODO dk:  make this prefetch data so we don't query like a horse in the desert without water that gets to an oasis its currently midnight he;p
    mentee_query = user_management_mentee_data.all().prefetch_related("account","mentor")
    for mentee in mentee_query:
        # Add needed mentee info to mentees list
        mentees.append({
            'account': mentee,
            'id': str(mentee),
            'mentor': mentee.mentor
        }) 
        
    context = {
        'mentees': mentees,
        'unaffiliated_mentors': [
                                    get_mentor_data_from_mentor(m,session_user) for m in 
                                    
                                    user_management_mentor_data.annotate(org_count=Count("organization")).filter(org_count=0).prefetch_related(
                                        "mentee_set","account","mentee_set__account"
                                        )
                                 ],
        'organizations': organizations,
        'role': session_user.str_role,

        'session_user_account': session_user,

        'user_admin_flag': session_user.is_super_admin(),
        'user_organization_admin_flag': session_user.is_an_org_admin()
    }

    render = template.render(context,request)

    return HttpResponse(render)


def get_mentor_data_from_mentor(mentor : 'Mentor',session_user : 'User')->dict:
    """
    convinece function that returns mentor data for the front end to use,
    I would muchly recommend going through the mentor objects themselfs if possible, but if this 
    is the prefered method this function makes it easier to work with :)
    """
    mentor_data = {
        'account': mentor,
        'id': str(mentor),
        #if you need the id mentor.account.id has it built in, so you don't need to pass it around twice,
        #still if you feel its better here uncomment :)
        #'id': str(mentor.account.id), #str(mentor.account), 
        
        #TODO:
        # we didn't see any usage usage of this while exploring, we also simplified the python
        # a bit to make it clearer what exactly this was passing over, we left the trailing , if
        # its needed anywhere (didn't see anything erroring with this commented out though)
        # if its still needed uncomment it :)
        # -dk
        'mentees': ",".join([str(m.account) for m in mentor._mentee_set.all()]),
        'current_mentees': mentor.mentee_set.count(),
        'max_mentees': mentor.int_max_mentees,

        # 'mentees': mentee_list,
        'mentor_admin_flag': session_user.is_super_admin() #auto caches :)
    }
    return mentor_data