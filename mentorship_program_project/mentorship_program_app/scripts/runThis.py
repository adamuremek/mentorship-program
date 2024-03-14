from mentorship_program_app.models import MentorshipRequest
from datetime import datetime

def run(): 
    # Users.objects.all().delete()
    # createUser('Admin2@svsu.edu', '', Users.Role.ADMIN,  'John', 'Doe', '999-888-7777', datetime(1998, 5, 17), 'Male', 'He/Him', '', '','bio')
    # # Create mentors
    # createUser('SueSmith@yahoo.com', '', Users.Role.MENTOR, 'Sue', 'Smith', '999-777-8888', datetime(1989, 12, 12), 'Female', 'She/Her', '', '','bio')
    # createUser('JasmineRodriguez@hotmail.com', '', Users.Role.MENTOR, 'Jasmine', 'Rodriguez', '888-777-9999',  datetime(1984, 11, 1), 'Female', 'She/Her', '', '','bio')
    # createUser('EmilyJohnson@gmail.com', '', Users.Role.MENTOR, 'Emily', 'Johnson', '555-123-4567', datetime(1994, 6, 20), 'Female', 'She/Her', '', '','bio')
    # createUser('DanielSmith@gmail.com', '', Users.Role.MENTOR, 'Daniel', 'Smith', '555-987-6543', datetime(1987, 11, 8), 'Male', 'He/Him', '', '','bio')
    # createUser('OliviaBrown@yahoo.com', '', Users.Role.MENTOR, 'Olivia', 'Brown', '555-456-7890', datetime(1990, 1, 15), 'Female', 'She/Her', '', '','bio')
    # # Create mentees
    # createUser('EthanWilson@svsu.edu', '', Users.Role.MENTEE, 'Ethan', 'Wilson', '555-321-6789', datetime(2000, 3, 12), 'Male', 'He/Him', '', '','bio')
    # createUser('ChloeTaylor@svsu.edu', '', Users.Role.MENTEE, 'Chloe', 'Taylor', '555-876-5432', datetime(2002, 12, 3), 'Female', 'She/Her', '', '','bio')
    # createUser('JacobMartinez@svsu.edu', '', Users.Role.MENTEE, 'Jacob', 'Martinez', '555-234-5678', datetime(2001, 8, 27), 'Male', 'He/Him', '', '','bio')
    # createUser('SophiaRodriguez@svsu.edu', '', Users.Role.MENTEE, 'Sophia', 'Rodriguez', '555-789-0123', datetime(2004, 5, 10), 'Female', 'She/Her', '', '','bio')
    # createUser('MiaLee@svsu.edu', '', Users.Role.MENTEE, 'Mia', 'Lee', '555-345-6789', datetime(2003, 11, 4), 'Female', 'She/Her', '', '','bio')
    
    # addInterests("A.I")
    # addInterests("Engineering")
    #addUserInterests(29,2)
    #print(getAllInterests())
    #print(getUserInformation(3))

    #mentorshipRequest.createRequest(1, 2)
    print(MentorshipRequest.get_request_info(1))
    #print(MentorshipRequest.removeRequest(4, 5))


    

    