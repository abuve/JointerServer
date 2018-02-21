# import the User object
#from django.contrib.auth.models import User
from user_center.models import UserProfile as User
import random
import string


def gen_random_pass(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size));


class spAuthBackend(object):


    def gen_id(size=32, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size));

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username):
        try:
            user = User.objects.get(username=username)
            print("USER EXISTS")
        except User.DoesNotExist:
            # Create a user in Django's local database
            print("USER NOT EXISTS")
            user = User.objects.create_user(username=username).set_unusable_password()
            user = User.objects.get(username=username)
            print ('test')
        except Exception as e:
            print(Exception, e)

        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None