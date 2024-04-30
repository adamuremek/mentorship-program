"""
/*********************************************************************/
/* FILE NAME: register_routes.py                                     */
/*********************************************************************/
/* PART OF PROJECT: Mentorship Program                               */
/*********************************************************************/
/* WRITTEN BY: A bunch of people                                     */
/* DATE CREATED:                                                     */
/*********************************************************************/
/* PROJECT PURPOSE:                                                  */
/*                                                                   */
/* This project aims to facilitate the mentorship registration       */
/* process within the platform, ensuring both mentors and mentees    */
/* can efficiently register and participate in mentorship activities.*/
/*********************************************************************/
/* FILE PURPOSE:                                                     */
/*                                                                   */
/* This file contains the functions necessary for the registration   */
/* of mentors and mentees, including rendering registration forms,   */
/* submitting registration data, and processing initial user setup.  */
/*********************************************************************/
/* DJANGO IMPORTED VARIABLE LIST (Alphabetically):                   */
/*                                                                   */
/* - HttpRequest: For obtaining details of HTTP requests             */
/* - HttpResponse, HttpResponseRedirect: Classes for sending HTTP responses */
/* - loader, Template: Utilities for rendering HTML templates        */
/* - ObjectDoesNotExist: Exception for handling non-existent objects */
/*********************************************************************/
/* MODIFICATION HISTORY:                                             */
/*********************************************************************/
/* Date       | Changed By | Changes Made                            */
/* -----------|------------|---------------------------------------- */
/*********************************************************************/
"""

import json
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader, Template
from mentorship_program_app.models import *
from .login_routes import login_uname_text
from django.utils.crypto import get_random_string
from .emails import *
from ..models import *
from typing import Dict
from utils import security

#@security.Decorators.validate_request_body("fname", "lname", "pronouns", "email", "phone-number", "password")
def register_mentor_submit(req: HttpRequest):
    
    '''
    Description
    -----------
    Function that will allow people to request to be a mentor.
    
    Parameters
    ----------
    - req : HttpRequest
    req should contain email (str), password (str), firstname (str), lastname (str), phone_number (str), pronouns (str), jobTitle (str), organization (str)
    
    Returns
    -------
    - str: Email {email} already exsists!
    - str: Registration request successful! We'll get back to ya!
    - str: Bad :(
    
    Example Usage
    -------------
    
    >>> reqister_mentor(req)
    "Email {email} already exsists!"
    
    >>> reqister_mentor(req)
    Registration request successful! We'll get back to ya!
    
    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    '''
    if req.method == "POST":
        incoming_email: str = req.POST["email"].lower()
        incoming_plain_text_password = req.POST["password"]

        # create a new user in the database with the role "Pending"
        pending_mentor_object = Mentor.create_from_plain_text_and_email(incoming_plain_text_password, incoming_email)
        
        # check if the account is already registered
        if pending_mentor_object == User.ErrorCode.AlreadySelectedEmail:
            return HttpResponse(f"Email {incoming_email} already exsists!")

        organization = None
        print("->> ", req.POST['company-name'])
        if req.POST['company-name'] and req.POST['company-name'] != "Other":
            print("HERE")
            organization_name = req.POST['company-name']
        else:
            organization_name = req.POST["organization"]
        print("org", organization_name)
        print("req: ", req.POST)
        if(not Organization.objects.filter(str_org_name=organization_name).exists()):
            organization = Organization.objects.create(str_org_name=organization_name)
            organization.save()

        else:
            organization = Organization.objects.get(str_org_name=organization_name)
            
        pending_mentor_object.account.cls_email_address = incoming_email
        pending_mentor_object.account.str_first_name = req.POST["fname"]
        pending_mentor_object.account.str_last_name = req.POST["lname"]
        pending_mentor_object.account.str_phone_number = f'{req.POST["phone_country_code"]} {req.POST["phone"]}'
        pending_mentor_object.account.str_preferred_pronouns = req.POST["pronouns1"] + '/' + req.POST["pronouns2"]

        #were not getting the data from the incoming form
        #if this is a thing we need to keep track of we should prolly send it
        #idk tho do whatevs -dk
        #str_gender = str_gender,


        user_mentor = User.objects.get(cls_email_address = incoming_email)
        
        pending_mentor_object.str_job_title =  req.POST["jobTitle"]
        pending_mentor_object.str_experience = req.POST["experience"]
        pending_mentor_object.organization.add(organization)

        parsed_user_interests = [
                                    Interest.get_or_create_interest(interest) for interest in req.POST.getlist("selected_interests")
                                 ]


        pending_mentor_object.account.save()
        pending_mentor_object.save()

        for interest in parsed_user_interests:
            pending_mentor_object.account.interests.add(interest)


        pending_mentor_object.save()
        
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTOR_REGISTER_EVENT, specified_user=user_mentor)
        mentor_signup_email(pending_mentor_object.account.cls_email_address)
        template: Template = loader.get_template('sign-in card/mentor/account_activation_mentor.html')
        ctx = {}
        
        return HttpResponse(template.render(ctx, req))
        
    else:
        return HttpResponse("Bad :(")
    
def register_mentee_submit(req: HttpRequest):
    
    '''
    Description
    -----------
    Function that will allow people to request to be a mentee.
    
    Parameters
    ----------
    - req : HttpRequest
    req should contain email (str), password (str), firstname (str), lastname (str), phone_number (str), pronouns (str)
    
    Returns
    -------
    - str: Email {email} already exsists!
    - HttpResponseRedirect:  ̶R̶e̶g̶i̶s̶t̶r̶a̶t̶i̶o̶n̶ ̶r̶e̶q̶u̶e̶s̶t̶ ̶s̶u̶c̶c̶e̶s̶s̶f̶u̶l̶!̶ ̶W̶e̶'̶l̶l̶ ̶g̶e̶t̶ ̶b̶a̶c̶k̶ ̶t̶o̶ ̶y̶a̶! now redirects the new user to their dashboard
    - str: Bad :(
    
    Example Usage
    -------------
    
    >>> reqister_mentee(req)
    "Email {email} already exsists!"
    
    >>> reqister_mentee(req)
    Registration request successful! We'll get back to ya!
    
     Edits
    -------------
    -changed the response from plain text html to a login and redirect

    Authors
    -------
    Adam U. ʕ·͡ᴥ·ʔ
    Andrew P.
    Jordan A.
    Tanner W. 🦞
    '''
    if req.method == "POST":
        if req.user.is_authenticated:
            incoming_email: str = req.user.email.lower()
        else:   
            return HttpRequest ("You have no permission to use my app")
        # Uncomment this if we choose to use the file to verify mentee eligiblity
        ################################################################
            # DO NOT DELETE THE 2 LINES THAT ARE COMMENTED OUT BELOW
        ################################################################
        # if WhitelistedEmails.objects.filter(str_email=incoming_email).count() == 0:
        #     return HttpResponse(json.dumps({"warning":"You are currently ineligible to use WINGS"}))
        incoming_plain_text_password = req.POST["password"]

        # create a new user in the database with the role "Pending"
        pending_mentee_object = Mentee.create_from_plain_text_and_email(incoming_plain_text_password, incoming_email)

        # check if the account is already registered
        if pending_mentee_object == User.ErrorCode.AlreadySelectedEmail:
            return HttpResponse(f"Email {incoming_email} already exsists!")
   
        pending_mentee_object.account.cls_email_address = incoming_email
        pending_mentee_object.account.str_first_name = req.POST["fname"]
        pending_mentee_object.account.str_last_name = req.POST["lname"]
        pending_mentee_object.account.str_preferred_pronouns = req.POST["pronouns1"] + '/' + req.POST["pronouns2"]

        parsed_user_interests = [
                                    Interest.get_or_create_interest(interest) for interest in req.POST.getlist("selected_interests")
                                ]

        


        for interest in parsed_user_interests:
            pending_mentee_object.account.interests.add(interest)

        
        pending_mentee_object.account.save()
        pending_mentee_object.save()

        user_mentee = User.objects.get(cls_email_address = incoming_email)
        SystemLogs.objects.create(str_event=SystemLogs.Event.MENTEE_REGISTER_EVENT, specified_user= User.objects.get(id=user_mentee.id))



        ##adds info to req with correct data names for the login function to work
        req._body = json.dumps({"username": incoming_email, "password": incoming_plain_text_password}).encode("utf-8")
        ##logins in the user
        return login_uname_text(req)

    else:
        return HttpResponse("Bad :(")
    


def register_mentor_render(req):
    template = loader.get_template('sign-in card/single_page_mentor.html')
    is_mentee : bool = False
    if not Interest.objects.exists():
        Interest.create_default_interests()

    if not Organization.objects.exists():
        Organization.create_default_company_names()

    
    country_codes : Dict
    with open('mentorship_program_app/routes/countries.json', 'r') as file:
        country_codes = json.load(file)
        country_codes = sorted(country_codes, key=lambda item: item["dial_code"])

    
    org_data_set = Organization.objects.all().values()
    # Truncates when above 20 characters and appends '...'
    companynames = [{'str_org_name': org_data['str_org_name'][:20] + "..." if len(org_data['str_org_name']) > 20 else org_data['str_org_name']} for org_data in Organization.objects.all().values()]

    org_data_json = json.dumps(list(org_data_set))
    
    
    context = {
        'user' : None,
        'is_mentee' : is_mentee,
        'interestlist': Interest.objects.all(),

        'pronounlist1': ['', 'he', 'she', 'they'],
        'pronounlist2': ['', 'him', 'her', 'them'],
        
        'country_codes' : country_codes,

        'companyname' : companynames, # org_data_set.all()
        'companyLIST': org_data_json,

        'companytypelist': [
            'Academic Research Group',
            'Aerospace Engineering',
            'Agriculture',
            'Automotive',
            'Banking',
            'Business Process Outsourcing',
            'Chemical Engineering',
            'College or University',
            'Construction',
            'Cybersecurity',
            'Digital Marketing',
            'E-commerce',
            'Energy and Utilities',
            'Entertainment',
            'Finance',
            'Government Agency',
            'Industrial Automation',
            'Insurance',
            'Internet Service Provider (ISP)',
            'IT Consulting',
            'IT Services',
            'Logistics',
            'Manufacturing',
            'Medical',
            'Mobile App',
            'Multimedia',
            'Nonprofit',
            'Payment Processing',
            'Pharmaceutical',
            'Public Health',
            'Real Estate',
            'Robotics',
            'Satellite Communication Provider',
            'Smart Home',
            'Software Development Consulting',
            'Sports Management',
            'Sporting Events',
            'Streaming Platform',
            'Transportation',
            'Telemedicine',
            'Video Game Development',
            'Virtual Reality',
            'Wireless Communication Provider'],
        
        # If this needs to be changed
        # also change it in the mentor mentee group page
        'experiencelist': [
            '0-4 years',
            '5-9 years', 
            '10+ years',
            ],

        'useragreement': 
           '''
End User License Agreement
<br><br>
1. Acceptance of Terms<br>
By accessing and using WINGS, you agree to be bound by this Agreement. If you do not agree to the terms of this Agreement, do not use the application. 
<br><br>
2. Description of Service<br>
WINGS provides a social networking platform that connects mentors and mentees for the purpose of educational and professional development. Features include profile creation, messaging, post sharing, and community interaction.
<br><br>
3. User Obligations<br>
You agree to provide accurate and complete information when creating your profile and to update your information as necessary.
You agree to use the application for lawful purposes only and to respect the rights and dignity of other users.
<br><br>
4. Privacy Policy<br>
Our Privacy Policy, which describes how we handle your personal data, is incorporated into this Agreement by reference.
<br><br>
5. Intellectual Property<br>
All content provided on the application is the proprietary property of the application developers or its users with all rights reserved unless otherwise stated.
Users may post content as long as it does not infringe on the intellectual property rights of others.
<br><br>
6. User Content<br>
You retain all rights to any content you submit, post, or display on or through the application.
You grant the application a non-exclusive, royalty-free license to use, copy, reproduce, process, adapt, modify, publish, transmit, display, and distribute such content in any and all media or distribution methods.
<br><br>
7. Prohibited Conduct<br>
You are responsible for all your activity in connection with the service.
You may not use the service for any illegal purpose or in any manner inconsistent with the terms of this Agreement.
<br><br>
8. Termination<br>
We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
<br><br>
9. Disclaimer of Warranties<br>
The service is provided on an "as is" and "as available" basis. Your use of the service is at your own risk.
We disclaim all warranties, express or implied, of merchantability, fitness for a particular purpose, or non-infringement.
<br><br>
10. Limitation of Liability<br>
To the fullest extent permitted by law, in no event shall the application, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the service.
<br><br>
11. Changes to Terms<br>
We reserve the right, at our sole discretion, to modify or replace these terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect.
<br><br>
12. Governing Law<br>
This Agreement shall be governed and construed in accordance with the laws of Michigan, United States, without regard to its conflict of law provisions.
<br><br>
Contact Us<br>
If you have any questions about this Agreement, please contact us at [Contact Information].
<br><br>
''',
    }
    return HttpResponse(template.render(context, req))


def register_mentee_render(req):
    template = loader.get_template('sign-in card/single_page_mentee.html')
    is_mentee : bool = True
    if not Interest.objects.exists():
        Interest.create_default_interests()
    
    # import os
    # print(os.getcwd())
    country_codes : Dict
    with open('mentorship_program_app/routes/countries.json', 'r') as file:
        country_codes = json.load(file)
        country_codes = sorted(country_codes, key=lambda item: item["dial_code"])
        
    
    context = {
        'is_mentee' : is_mentee,
        
        'interestlist':  Interest.objects.all(),
        
        'menteeEmailMessage': "You MUST use your SVSU.EDU email address.",
        
        'pronounlist1': ['', 'he', 'she', 'they'],
        'pronounlist2': ['', 'him', 'her', 'them'],
        
        'country_codes' : country_codes,
        
        'useragreement': 
            '''
End User License Agreement
<br><br>
1. Acceptance of Terms<br>
By accessing and using WINGS, you agree to be bound by this Agreement. If you do not agree to the terms of this Agreement, do not use the application. 
<br><br>
2. Description of Service<br>
WINGS provides a social networking platform that connects mentors and mentees for the purpose of educational and professional development. Features include profile creation, messaging, post sharing, and community interaction.
<br><br>
3. User Obligations<br>
You agree to provide accurate and complete information when creating your profile and to update your information as necessary.
You agree to use the application for lawful purposes only and to respect the rights and dignity of other users.
<br><br>
4. Privacy Policy<br>
Our Privacy Policy, which describes how we handle your personal data, is incorporated into this Agreement by reference.
<br><br>
5. Intellectual Property<br>
All content provided on the application is the proprietary property of the application developers or its users with all rights reserved unless otherwise stated.
Users may post content as long as it does not infringe on the intellectual property rights of others.
<br><br>
6. User Content<br>
You retain all rights to any content you submit, post, or display on or through the application.
You grant the application a non-exclusive, royalty-free license to use, copy, reproduce, process, adapt, modify, publish, transmit, display, and distribute such content in any and all media or distribution methods.
<br><br>
7. Prohibited Conduct<br>
You are responsible for all your activity in connection with the service.
You may not use the service for any illegal purpose or in any manner inconsistent with the terms of this Agreement.
<br><br>
8. Termination<br>
We may terminate or suspend your account and bar access to the service immediately, without prior notice or liability, under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach of the Terms.
<br><br>
9. Disclaimer of Warranties<br>
The service is provided on an "as is" and "as available" basis. Your use of the service is at your own risk.
We disclaim all warranties, express or implied, of merchantability, fitness for a particular purpose, or non-infringement.
<br><br>
10. Limitation of Liability<br>
To the fullest extent permitted by law, in no event shall the application, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the service.
<br><br>
11. Changes to Terms<br>
We reserve the right, at our sole discretion, to modify or replace these terms at any time. If a revision is material, we will provide at least 30 days' notice prior to any new terms taking effect.
<br><br>
12. Governing Law<br>
This Agreement shall be governed and construed in accordance with the laws of Michigan, United States, without regard to its conflict of law provisions.
<br><br>
Contact Us<br>
If you have any questions about this Agreement, please contact us at [Contact Information].
<br><br>
''',

        'user': req.user,
        # # TODO: replace this or get rid of password for mentees. 
        # # For now it is just generating a password so I can test without modifying validation code
        'random_password': get_random_string(length=30) + "1A!",
    }
    return HttpResponse(template.render(context, req))