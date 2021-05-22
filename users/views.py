import jwt, bcrypt, json

from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError

from projects.models import Site
from .serializers import DriverSerializer, DriverViewSerializer
from .models import Driver, Admin
from .serializers import AdminSerializer

from my_settings import SECRET_KEY, algorithms
from utils import login_required
from pagination import MyPagination


class SignupView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request):
        try:
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
                 'exp': datetime.utcnow() + timedelta(seconds=30000)}, SECRET_KEY,
                algorithm=algorithms)

            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK, headers={'token': access_token})
        except:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)


class DriverView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user
        serializer_class = DriverViewSerializer
        self.pagination_class.page_size = request.GET.get('limit', 10)
        if admin.type == 'ProjectTotalAdmin':
            queryset = Driver.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Driver.objects.filter(is_active=True, site__site_admin__pk=admin.pk)
        page = self.paginate_queryset(queryset)
        serializer = serializer_class(page, many=True)
        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            if Driver.objects.filter(phone_number=request.data['phone_number']).exists():
                return Response({'message': 'DUPLICATE_PHONE_NUMBER'}, status=status.HTTP_409_CONFLICT)
            if not request.user.site.filter(pk=request.data['site']).exists():
                return Response({'message': 'INVALID_SITE'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = DriverSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        try:
            if request.data.get('driver_id') is None:
                return Response({'message': 'CHECK_DRIVER_ID'}, status=status.HTTP_400_BAD_REQUEST)

            driver = Driver.objects.get(pk=request.data['driver_id'])
            serializer = DriverSerializer(driver, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Driver.DoesNotExist:
            return Response({'message': 'DRIVER_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    def delete(self, request, driver_id):
        try:
            driver = Driver.objects.get(pk=driver_id, is_active=True)
            driver.is_active = False
            driver.save()
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_205_RESET_CONTENT)
        except Driver.DoesNotExist:
            return Response({'message': 'DRIVER_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
