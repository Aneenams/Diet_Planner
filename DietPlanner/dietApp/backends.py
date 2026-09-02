from django.contrib.auth.backends import BaseBackend
from dietApp.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user_obj=User.objects.get(email=username)
            if user_obj.check_password(password):
                return user_obj
            else:
                return None
        except:
            return None    

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None    

class PhoneBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user_obj=User.objects.get(phone=username)
            if user_obj.check_password(password):
                return user_obj
            else:
                return None
        except:
            return None    

    def get_user(self,user_id):
            try:
                return User.objects.get(id=user_id)
            except:
                return None                 