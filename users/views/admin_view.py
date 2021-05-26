from datetime import datetime, timedelta

import bcrypt
import jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.admin import Admin, AdminSerializer

from my_settings import SECRET_KEY, algorithms


class SignupView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request):
        data = request.data
        account_name = data['account_name']
        password = data['password']

        if not Admin.objects.filter(account_name=account_name).exists():
            return Response({'message': 'ACCOUNT_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

        admin = Admin.objects.get(account_name=account_name)

        if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
            return Response({'message': 'INVALID_PASSWORD'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = jwt.encode(
            {'admin_id': admin.pk,
             'exp': datetime.utcnow() + timedelta(seconds=30000000)}, SECRET_KEY,
            algorithm=algorithms)

        return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK, headers={'token': access_token})
