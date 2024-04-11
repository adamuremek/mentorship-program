from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest
from ..models import User


from_email = settings.EMAIL_HOST_USER

def notifications_on(email : str):
	user = User.objects.get(cls_email_address=email)
	if user.bln_notifications:
		return True
	else:
		return False
	


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


def reset_token_email(request: HttpRequest, recipient: str, token: str):
	subject = "WINGS Password Reset Link"
	domain = request.get_host()
	reset_link = f"http://{domain}/request_reset_page/{token}"
	message = f"""
	Please <a href="{reset_link}">Click Here</a> to reset your WINGS password.
	"""
	send_mail(subject, message, from_email, [recipient], html_message=message)


def alert_admins_of_reported_user():
	admins = User.objects.filter(str_role="Admin").values_list('cls_email_address', flat=True)
	subject = "⚠️ User Reported ⚠️"
	message = """
	Hello Admins,

	A user has been reported and action is required. Please review and take action in the application.
	"""
	send_mail(subject, message, from_email, admins)


def email_for_mentorship_acceptance(mentor_email : str, mentee_email : str):
	recipients = [mentor_email, mentee_email]
	if not notifications_on(mentor_email):
		recipients.remove(mentor_email)
	if not notifications_on(mentee_email):
		recipients.remove(mentee_email)

	if len(recipients) == 0:
		return
	subject = "Mentorship Created!"
	message = """
	Hello,

	This email is to inform you of a new mentorship!

	Please visit the application and navigate to view your new mentorship

	Thanks,

	WINGS
	"""
	send_mail(subject, message, from_email, recipients)

def email_for_mentorship_rejection(recipient: str):
	if not notifications_on(recipient):
		return
	subject = "Mentorship Rejected!"
	message = """
	Hello,

	This email is to inform you of that one of your mentorships has been declined. This may be for a number of reasons. Please visit the WINGS app to explore other potential mentorships.

	Thanks,

	WINGS
	"""
	send_mail(subject, message, from_email, [recipient])

def your_mentor_quit(recipient: str, opposite_role: str):
		if not notifications_on(recipient):
			return
		subject = "Important Info"
		message =f"""
		Hello,

		This email is to inform you that your	{opposite_role} is no longer apart of the WINGS program. If you wish to start a new mentorship, please visit the WINGS app to find a new {opposite_role}.

		Thanks,

		WINGS
	"""
		send_mail(subject, message, from_email, [recipient])
		
def you_have_a_new_request(recipient: str):
		if not notifications_on(recipient):
			return
		subject = "You have a new mentorship request!"
		message =f"""
		Hello,

		This email is to inform you that have a new mentorship request! Visit the WINGS app to check it out!

		Thanks,

		WINGS
	"""
		send_mail(subject, message, from_email, [recipient])
		