from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Location, Site
from .serializers import SiteSerializer, SiteViewSerializer, LocationSerializer, LocationViewSerializer

from utils import login_required
from pagination import MyPagination


class SiteView(APIView):
    def post(self, request):
        a = request.data['start_date']
        b = request.data['end_date']

        if a > b:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

        if Site.objects.filter(name=request.data['name']).exists():
            return Response({'message': 'NAME_EXIST'}, status=status.HTTP_409_CONFLICT)

        serializer = SiteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            sites = Site.objects.filter(is_active=True)
            serializer = SiteViewSerializer(sites, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Site.DoesNotExist:
            return Response({'message': 'DATA_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            if Site.objects.filter(pk=request.data['site_id']).exists():
                site = Site.objects.get(pk=request.data['site_id'])

            serializer = SiteSerializer(site, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, site_id):
        try:
            site = Site.objects.get(pk=site_id, is_active=True)
            site.is_active = False
            site.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

        except Site.DoesNotExist:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)


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
