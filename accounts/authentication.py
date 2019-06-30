from accounts.models import User, Token
import sys

class PasswordlessAuthenticationBackend(object):
    def authenticate(self,request, uid):
        print('Authenticate...', file=sys.stderr)
        try:
            token = Token.objects.get(uid=uid)
            print('W try', file=sys.stderr)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            print('W user does not exist', file=sys.stderr)
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            print('Brak tokenu', file=sys.stderr)
            return None
        
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        