"""
    Description
    -----------
    This is a simple script to test the basic functionality 
    of a One Time Password (OTP) system for the mentor MFA.

    How to Run
    ----------
    Replace str_test_email and str_test_password with an email and password.
    In the console 
    Navigate to ..\mentorship-program\mentorship_program_project
    Then run `python manage.py runscript mentor_mfa`

    Success will output "GOOOOOD MORNING NIGHT CITY!"

    Optional: set bool_debug from False to True to skip the 'login' part.

    Authur
    ------
    Justin Goupil

    Note: add to git ignore
"""

from datetime import datetime, timedelta
from getpass import getpass

import pyotp
import time
from django.core.mail import send_mail

def run(): 

    bool_debug = False

    str_test_email = "" #Replace with your email.
    str_test_password = "" #Replace with your password.
    str_message = None
    int_interval = 60 * 5 #Seconds * Minutes
    int_minutes = 1 # Minutes

    str_otp_input = None

    totp = pyotp.TOTP(pyotp.random_base32(), interval= int_interval * 10) #Interval in seconds
    #One Time Password
    otp = totp.now()
    otp_secret_key = totp.secret

    str_valid_until = str(datetime.now() + timedelta(minutes=int_minutes))

    print("Hello World!\nEnter your username and password below:")
    
    if bool_debug:
        str_email = str_test_email
        str_password = str_test_password
    else:
        str_email = input("Email: ")
        str_password = getpass("Password: ")
    

    if str_email == str_test_email and str_password == str_test_password:
        #Print the OTP generated to the console.
        print("Your one time password is " +otp+".")

        #Send the one time password to the email address.
        send_mail(
            "WINGS Sign-in Code",
            "Your one time password is: " + otp,
            "",
            [str_email],
            fail_silently=False
            )

        #Prompt for OTP
        str_otp_input = input("Enter your one time password: ")

        #time.sleep(60)

        #Check for valid date
        if datetime.fromisoformat(str_valid_until) > datetime.now():
            #Check the security key            
            if totp.verify(str_otp_input):
                str_message = "GOOOOOD MORNING NIGHT CITY!"
            else:
                str_message = "Verify Failed"
        else:
            str_message = "TIME OUT"
    else:
        str_message = "No future"

    print(str_message)
