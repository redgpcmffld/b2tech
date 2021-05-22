from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LocationSerializer, LocationViewSerializer
from .models import Location, Site
from utils import login_required
from pagination import MyPagination


class LocationView(APIView, MyPagination):
    @login_required
    def get(self, request):
        try:
            admin = request.user
            if admin.type == 'ProjectTotalAdmin':
                queryset = Location.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
            else:
                queryset = Location.objects.filter(is_active=True, site__site_admin__pk=admin.pk)
            serializer_class = LocationViewSerializer
            self.pagination_class.page_size = request.GET.get('limit', 10)
            page = self.paginate_queryset(queryset)
            serializer = serializer_class(page, many=True)
            return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                             'result': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def post(self, request):
        if Location.objects.filter(
                name=request.data['name'],
                type=request.data['type']).exists():
            return Response({'message': 'DUPLICATE_LOCATION'}, status=status.HTTP_409_CONFLICT)
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        try:
            if request.data.get('location_id') is None:
                return Response({'message': 'CHECK_LOCATION_ID'}, status=status.HTTP_400_BAD_REQUEST)

            location = Location.objects.get(pk=request.data['location_id'])
            serializer = LocationSerializer(location, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({'message': 'LOCATION_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    def delete(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id, is_active=True)
            location.is_active = False
            location.save()
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)
        except Location.DoesNotExist:
            return Response({'message': 'LOCATION_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
