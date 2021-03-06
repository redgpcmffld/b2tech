import jwt

from rest_framework.response import Response
from rest_framework import status
from users.models.admins import Admin

from my_settings import algorithms, SECRET_KEY


def login_required(func):
    def decorator(self, request, *args, **kwargs):
        try:
            if request.headers.get('Authorization') is None:
                return Response({'message': 'TOKEN_NOT_FOUND'}, status=status.HTTP_400_BAD_REQUEST)
            access_token = request.headers['Authorization']
            user = jwt.decode(access_token, SECRET_KEY, algorithms=algorithms)
            request.user = Admin.objects.get(pk=user['admin_id'])

            return func(self, request, *args, **kwargs)

        except jwt.InvalidKeyError:
            return Response({"message": "INVALID_LOGIN"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"message": "INVALID_TOKEN"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return Response({'message': 'EXPIRED_TOKEN'}, status=status.HTTP_401_UNAUTHORIZED)

    return decorator
