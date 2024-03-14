"""
Description
-----------
Creates a sample of Users and relations for the database and saves them to the database.
"""

from mentorship_program_app.models import *
from datetime import datetime

def run():
    print("Hello, creating a list of users. Please wait.")
    list_of_users = []
    list_of_users.append( 
        create_user( "fryan3@svsu.edu", "Qwerty123!@#", User.Role.MENTEE, datetime.now(), True, False, "Frank", "Ryan", "(256) 365-1024", datetime(2000,9,27), "Male", "Him/He"))
    # Create admin
    list_of_users.append(create_user('Admin2@svsu.edu', 'Qwerty123!@#', User.Role.ADMIN, datetime.now(),True, False, 'Scott', 'James', '999-888-7777', datetime(1998, 5, 17), 'Male', 'He/Him'))
    # Create mentors
    list_of_users.append(create_user('SueSmith@yahoo.com', 'Qwerty123!@#', User.Role.MENTOR, datetime.now(), True, False, 'Sue', 'Smith', '999-777-8888', datetime(1989, 12, 12), 'Female', 'She/Her'))
    list_of_users.append(create_user('JasmineRodriguez@hotmail.com', 'Qwerty123!@#', User.Role.MENTOR, datetime.now(), True, False, 'Jasmine', 'Rodriguez', '888-777-9999',  datetime(1984, 11, 1), 'Female', 'She/Her'))
    list_of_users.append(create_user('EmilyJohnson@gmail.com', 'Qwerty123!@#', User.Role.MENTOR, datetime.now(), True, False, 'Emily', 'Johnson', '555-123-4567', datetime(1994, 6, 20), 'Female', 'She/Her'))
    list_of_users.append(create_user('DanielSmith@gmail.com', 'Qwerty123!@#', User.Role.MENTOR, datetime.now(), False, True, 'Daniel', 'Smith', '555-987-6543', datetime(1987, 11, 8), 'Male', 'He/Him'))
    list_of_users.append(create_user('OliviaBrown@yahoo.com', 'Qwerty123!@#', User.Role.MENTOR, datetime.now(), False, True, 'Olivia', 'Brown', '555-456-7890', datetime(1990, 1, 15), 'Female', 'She/Her'))
    # Create mentees
    list_of_users.append(create_user('EthanWilson@svsu.edu', 'Qwerty123!@#', User.Role.MENTEE, datetime.now(), True, False, 'Ethan', 'Wilson', '555-321-6789', datetime(2000, 3, 12), 'Male', 'He/Him'))
    list_of_users.append(create_user('ChloeTaylor@svsu.edu', 'Qwerty123!@#', User.Role.MENTEE, datetime.now(), True, False, 'Chloe', 'Taylor', '555-876-5432', datetime(2002, 12, 3), 'Female', 'She/Her'))
    list_of_users.append(create_user('JacobMartinez@svsu.edu', 'Qwerty123!@#', User.Role.MENTEE, datetime.now(), True, False, 'Jacob', 'Martinez', '555-234-5678', datetime(2001, 8, 27), 'Male', 'He/Him'))
    list_of_users.append(create_user('SophiaRodriguez@svsu.edu', 'Qwerty123!@#', User.Role.MENTEE, datetime.now(), True, False, 'Sophia', 'Rodriguez', '555-789-0123', datetime(2004, 5, 10), 'Female', 'She/Her'))
    list_of_users.append(create_user('MiaLee@svsu.edu', 'Qwerty123!@#', User.Role.MENTEE, datetime.now(), True, False, 'Mia', 'Lee', '555-345-6789', datetime(2003, 11, 4), 'Female', 'She/Her'))
    
    #user1.create_from_plain_text_and_email("joeshmoe@gmail.com", "qwerty123")  
    #user = list_of_users[0].save()  
    print(list_of_users[0].cls_email_address)
    #print(User.objects.get())

    #for users in list_of_users:
    #    users.save()

    print("Users have been created.")

def create_user(
        email_address, plain_text_password,
        role, date_joined, active, account_disabled,
        first_name, last_name, phone_number, last_login_date, gender, pronoun):
    #Creates a database object called user.
    generated_salt = security.generate_salt()

    user = User(
    cls_email_address = email_address, 
    str_password_hash = security.hash_password(plain_text_password, generated_salt),
    str_password_salt = generated_salt,
    str_role = role,
    cls_date_joined = date_joined,
    bln_active = active,
    bln_account_disabled =  account_disabled,

    str_first_name = first_name,
    str_last_name = last_name, 
    str_phone_number = phone_number,
    str_last_login_date = last_login_date,
    str_gender = gender,
    str_preferred_pronouns = pronoun
    )

    return user