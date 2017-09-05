from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        hashes a password using pbkdf2_sha512
        :param password: the sha512 password from the login/register form
        :return: a sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        '''
        Checks that the password user sent matches the pw in the db
        The db pw is encrypted more than the user's at this stage
        :param password: sha512-hashed pw
        :param hashed_password: pbkdf2_sha512 encrypted
        :return: true if pws match else false
        '''

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile("^([\w-]+\.)+[\w-]+@([\w-]+\.)+[\w]+$")
        email_address_matcher_alt = re.compile("^[\w-]+[\w-]+@([\w-]+\.)+[\w]+$")
        if email_address_matcher.match(email) or email_address_matcher_alt.match(email):
            return True
