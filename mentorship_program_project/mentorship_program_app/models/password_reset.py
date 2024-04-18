from django.db import models
from django.db.models import *
from django.core.exceptions import ObjectDoesNotExist
from .user import User
import random
import string
from utils import security
from django.utils import timezone
from datetime import timedelta
from typing import Tuple


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, unique=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_reset_token(user_id):
        try:
            # Get the user instance
            user_instance = User.objects.get(pk=user_id)

          # Check if the user already has a token, delete it if it exists
            try:
                existing_token = PasswordResetToken.objects.get(user=user_id)
                existing_token.delete()
            except ObjectDoesNotExist:
                # No existing token for the user, proceed with creating a new one
                print("Existing link deleted")
                pass



            

            duplicate = True
            token = ""
            while duplicate:
                # Define the pool of characters to choose from (only uppercase letters and digits)
                characters = string.ascii_uppercase + string.digits

                # Generate a random string of length 6
                token = ''.join(random.choice(characters) for _ in range(30))

                #checks to see if token exist already
                duplicate = PasswordResetToken.objects.filter(token=token).exists()
            
            reset_token_instance = PasswordResetToken(user=user_instance, token=token)
            # Save the new instance of PasswordResetToken model
            reset_token_instance.save()

            return True, "Reset link created successfully", token
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, f"An error occurred creating your link", token
        

    
    def is_valid_token(self) -> Tuple[bool, str]: #this deletes a token if its not valid
        try:
            expiration_time = 10 ## time for a token to expire in minutes

            # Get the current time
            current_time = timezone.now()
        
            # Calculate the timestamp ten minutes ago
            ten_minutes_ago = current_time - timedelta(minutes=expiration_time)
        
            # Check if the token timestamp is greater than or equal to ten minutes ago
            if self.timestamp >= ten_minutes_ago:
                # Token is valid
                return True , "found"
            else:
                # Token expired
                self.delete() #delete expired tokens
                return False, "expired"
        except Exception as e:
            # Log or handle the exception
            return False, "ex"
    
    #deletes all expired tokens by validating them
    @staticmethod
    def delete_all_expired_reset_tokens():
        tokens = PasswordResetToken.objects.all()

        for token_record in tokens:
            if not token_record.is_valid_token(token_record):
                print(f"Expired token deleted: {token_record}")
            else:
                print(f"Token is still valid: {token_record}")

    @staticmethod
    def validate_and_reset_password(token: str, new_password: str) -> Tuple[bool, str]:
        try:
            # Retrieve the token instance based on user ID and token

          
            token_instance = PasswordResetToken.objects.get(token=token)
            
            
            valid, message = token_instance.is_valid_token()
            # Check if the token is valid
            if not valid:
                if message == "expired":
                    return False,  "Link expired, attempt reset again!"
                if message == "ex":
                    return False, "An error occoured verifying your link."
            # Delete the token since it was correct and is no longer needed
            

            user = User.objects.get(id=token_instance.user.id)
            generated_user_salt = security.generate_salt()
            user.str_password_hash = security.hash_password(new_password, generated_user_salt)
            user.str_password_salt = generated_user_salt
            user.save()
            token_instance.delete()

            
            return True, "Password successfully reset, Rerouting you to home page."  # Password reset successful
        except PasswordResetToken.DoesNotExist:
            return False,  "Invalid Link"