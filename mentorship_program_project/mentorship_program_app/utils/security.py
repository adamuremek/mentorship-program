import bcrypt

"""
"peppering" a password string is a technique that can provide
a moderate level of additional security in the hashing process by 
removing dependencies on database leaks.

See: https://security.stackexchange.com/questions/17421/how-to-store-salt
for more information regaurding salting and peppering
"""
strPepper : str = """peter pipper 
            picked a 
            pack of 
            pickled peppers 
            to replace 
            this text 
            and make it more secure :D"""
"""
    hashes an incoming plain text password using the applications built in pepper and 
    provided salt.
    In order for the peppering to work this should be the one stop shop for hashing
"""
def hash_password(password_plain_text : str,salt : str)->str:
    return bcrypt.hashpw(password_plain_text + pepper ,salt)
