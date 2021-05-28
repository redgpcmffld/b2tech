from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.site import Site
from ..models.driver import Driver, DriverSerializer, DriverViewSerializer

from utils import login_required
from pagination import MyPagination


class DriverView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user
        self.pagination_class.page_size = request.GET.get('limit', 10)
        if admin.type == 'ProjectTotalAdmin':
            queryset = Driver.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Driver.objects.filter(is_active=True, site__site_admin__pk=admin.pk)
        page = self.paginate_queryset(queryset)
        serializer = DriverViewSerializer(page, many=True)
        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            if Driver.objects.filter(phone_number=request.data['phone_number']).exists():
                return Response({'message': 'DUPLICATE_PHONE_NUMBER'}, status=status.HTTP_409_CONFLICT)

            serializer = DriverSerializer(data=request.data, context={'admin': request.user})

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
            serializer = DriverSerializer(driver, data=request.data, context={'admin': request.user})

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
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            return Response({'message': 'DRIVER_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
