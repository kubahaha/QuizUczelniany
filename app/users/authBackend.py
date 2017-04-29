from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserModelUsernameEmailBacked(object):
    def authenticate(self, request, login=None, password=None):
        if login is None or password is None:
            return None

        if UserModel.objects.filter(username=login).exists():
            user_instance = UserModel.objects.filter(username=login)[0]
        elif UserModel.objects.filter(email=login).exists():
            user_instance = UserModel.objects.filter(email=login)[0]
        else:
            return None

        if user_instance.check_password(password):
            return user_instance
        else:
            return None

    def get_user_by_id(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user
