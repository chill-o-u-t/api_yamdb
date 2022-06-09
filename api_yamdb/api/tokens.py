from rest_framework_simplejwt.tokens import AccessToken


def get_tokens_for_user(user):
    return {
        'token': str(AccessToken.for_user(user)),
    }
