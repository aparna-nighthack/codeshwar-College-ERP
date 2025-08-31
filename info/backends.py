from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class PasswordOnlyBackend(BaseBackend):
    """
    Authenticate any username when the password is exactly 'password'.

    For development/testing only. Do not use in production.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Support authentication with multiple username keywords (e.g., via AuthenticationForm)
        if username is None:
            username = kwargs.get(get_user_model().USERNAME_FIELD)

        if password != 'password' or not username:
            return None

        User = get_user_model()
        user, _ = User.objects.get_or_create(username=username)
        if not user.is_active:
            return None
        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

