from django.core.management.base import BaseCommand, CommandError
from mentorship_program_app.models import SuperAdminEntry,User
from getpass import getpass



class Command(BaseCommand):
    """
    Description
    -----------
    Custom django-admin command that creates a Super Administrator
    and adds them to the database.

    Properties
    ----------
    help = Displays string of information when
           `python manage.py --help` is ran.

    Instance Functions
    -------------------
    prompt_password_plain_text : Prompts the user to enter a password in plain text.
    prompt_email : Prompts the user to enter an email.
    handle : Executes the main body of code. Like main(String[] args) in Java. 

    Static Functions
    -------
    (None)

    Magic Functions
    -------------
     (None)

    Authors
    -------
    David Kennamer ⌨️
    Justin Goupil ♟️
    """
    help = "Run this to create a new super admin account in the database."


    def prompt_password_plain_text(self)->str:
        """
        Description
        -----------
        Prompts the user to enter a password.
        Uses python getpass to hide user's input.

        Parameters
        ----------
        self : Represents the instance of the class.

        Returns
        -------
        - password (string) : Password stored as plain text.

        Example Usage
        -------------

        >>> password = prompt_password_plain_text()
        console view {
            (admin password)>
            (confirm admin password)>
        }
        password = 3x@mple_pas$w0rd_5

        Authors
        -------
        David Kennamer ⌨️
        Justin Goupil ♟️
        """
        password = getpass('(admin password)> ')
        password2 = getpass('(confirm admin password)> ')

        while password != password2:
            print("[ERROR] your passwords did not match!")

            password = getpass('(admin password)> ')
            password2 = getpass('(confirm admin password)> ')

        return password

    def prompt_email(self)->str:
        """
        Description
        -----------
        Prompts the user to enter an email.

        Parameters
        ----------
        self : Represents the instance of the class.

        Returns
        -------
        - email (string) : email address.

        Example Usage
        -------------

        >>> email = prompt_email()
        console view {
            (email)> jmgoupil@svsu.edu
        }
        email = jmgoupil@svsu.edu

        Authors
        -------
        David Kennamer ⌨️
        Justin Goupil ♟️
        """
        return input("(email)> ")

    def handle(self, *args, **options):
        """
        Description
        -----------
        Prompts the user to enter an email.

        Parameters
        ----------
        self : Represents the instance of the class.
        *args : django method to pass arguments via command line.
        **options : django method to pass optional arguments via 
                    command line. Not used.

        Returns
        -------
        - NONE

        Example Usage
        -------------

        >>> handle()
        console view {
            (email)> sample@mail.com
            (admin password)> 
            (confirm admin password)>
            Super Admin account has been created.
            <End of Script>
        }
        A User and their relation in SuperAdminEntry is 
        created and saved to the database.

        Authors
        -------
        David Kennamer ⌨️
        Justin Goupil ♟️
        """
        admins = SuperAdminEntry.objects.all()

        if len(admins) > 0:
            print("[WARNING] there are already admins in the database, are you sure you wish to create an additional admin? ")
            ansr = input("(y/n)> ")
            if ansr != 'y':
                return False

        email = self.prompt_email()
        password_plain_text = self.prompt_password_plain_text()

        admin_user_account = User.create_from_plain_text_and_email(password_plain_text, email)
        admin_user_account.save()

        super_admin_entry = SuperAdminEntry.objects.create(user_account=admin_user_account,bool_enabled=True)
        super_admin_entry.save()

        print("Super Admin account has been created.")




