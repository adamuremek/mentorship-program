from django.core.mail import send_mail
from django.conf import settings

from_email = "wingsmentorapp@gmail.com"

def send_email_test():
	send_mail("WELCOME!", "welcome to da app", from_email, ["aruemek3@gmail.com"])


def mentor_signup_email(recipient : str):
	message = """
	Welcome to Wings!

	Thank you for registering as a mentor! We are thrilled to have you join our community.

	Your application is now under review by our administrative team. We carefully evaluate each application to ensure the best fit for our program and participants.

	You will receive an email notification regarding the outcome of your application once it has been decided. Please keep an eye on your inbox, including your spam folder, to ensure you don't miss any updates.

	In the meantime, we encourage you to explore our website and familiarize yourself with our program's mission, values, and upcoming events. Feel free to reach out to us if you have any questions or need assistance.

	Thank you again for your interest in Wings. We look forward to the possibility of working together to make a positive impact in our community.

	Best regards,
	Admin
"""

	send_mail("Welcome to Wings!", message, from_email, [recipient])


def mentor_denied_email(recipient : str):
    subject = "WINGS Mentor Application Status: Denied"
    message = """
    Dear Applicant,

    We regret to inform you that your application to become a mentor for the WINGS program has been denied. We appreciate your interest and effort in applying, but unfortunately, we have decided not to proceed with your application at this time.

    While we cannot provide specific reasons for the denial, please know that our decision was based on a careful review of your application and our program's needs. We encourage you to continue pursuing opportunities to contribute to our community and wish you the best in your future endeavors.

    Thank you again for your interest in the WINGS program.

    Sincerely,
    Admin
    """
    
    send_mail(subject, message, from_email, [recipient])
    
def mentor_accepted_email(recipient : str):
	subject = "WINGS Mentor Application Status: Accepted"
	message = """
	Congratulations and Welcome to WINGS!

	We are thrilled to inform you that your application to become a mentor for the WINGS program has been accepted. Welcome aboard!

	Your dedication to making a positive impact in our community is commendable, and we are excited to have you join our team of mentors. Together, we will work towards empowering and supporting our participants to reach their full potential.

	As a mentor, you play a vital role in shaping the lives of our program participants. Your guidance, support, and expertise will make a significant difference in their journey towards success.

	To begin, sign in to your account and begin filling out your profile.

	Once again, congratulations on your acceptance into the WINGS program. We look forward to working closely with you and making a meaningful impact together.

	Best regards,
	Admin
	"""
	send_mail(subject, message, from_email, [recipient])


def reset_token_email(recipient : str, token : str):
	subject = "WINGS Password Reset Token"
	message = f"""
	Heres your token bitch {token}
	Please go to http://localhost:8000/request_reset_page and enter your token to reset your password
	"""
	send_mail(subject, message, from_email, [recipient])



