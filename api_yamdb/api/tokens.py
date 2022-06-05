from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from rest_framework_simplejwt.tokens import AccessToken


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        print(user)
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_tokens_for_user(user):
    token = AccessToken.for_user(user)

    return {
        'token': str(token),
    }
