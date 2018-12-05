import jwt
from django.conf import settings
import datetime
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions

"""Configure JWT Here"""


secret_key = settings.SECRET_KEY


class Authentication(JSONWebTokenAuthentication):

    @staticmethod
    def generate_jwt_token(user, refresh_token=False):
        """ method to generate token """

        token = jwt.encode({
            "username": user["username"],
            "refresh_token": refresh_token,
            "iat": datetime.datetime.utcnow(),
            'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, secret_key)
        token = str(token, 'utf-8')
        return token

    @staticmethod
    def decode_jwt_token(token):
        try:
            user_info = jwt.decode(token, secret_key)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired please request for another')
        return user_info
