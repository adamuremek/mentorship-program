from django.core.management.base import BaseCommand, CommandError
from mentorship_program_app.models import SuperAdminEntry,User
from getpass import getpass



class Command(BaseCommand):
    help = "run this to create a new super admin account in the database"


    def prompt_password_plain_text(self)->str:
        password = getpass('(admin password)> ')
        password2 = getpass('(confirm admin password)> ')

        while password != password2:
            print("[ERROR] your passwords did not match!")

            password = getpass('(admin password)> ')
            password2 = getpass('(confirm admin password)> ')

        return password

    def prompt_email(self)->str:
        return input("(email)> ")

    def handle(self, *args, **options):
        admins = SuperAdminEntry.objects.all()
        if len(admins) > 0:
            print("[WARNING] there are already admins in the database, are you sure you wish to create an additional admin? ")
            ansr = input("(y/n)> ")
            if ansr != 'y':
                return False

        email = self.prompt_email()
        password_plain_text = self.prompt_password_plain_text()

        admin_user_account = User.create_from_plain_text_and_email(password_plain_text, email)
        admin_user_account = User.Role.ADMIN
        admin_user_account.save()

        super_admin_entry = SuperAdminEntry.objects.create(user_account=admin_user_account,bool_enabled=True)
        super_admin_entry.save()




