from django.db.models import Sum, Max

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from haversine import haversine

from .models import DriveRecord, DriveRoute
from projects.models import Project, Site, Location
from .serializers import (
    DriveStartSerializer,
    DriveRecordViewSerializer,
    DriveEndSerializer,
    ProgressSerializer,
    DriveRouteSerializer,
    DriveRouteViewSerializer
)
from utils import login_required
from pagination import MyPagination


class DriveStartView(APIView):
    @login_required
    def post(self, request):
        if Location.objects.get(pk=request.data.get('loading_location')).resource.get().pk != Location.objects.get(
                pk=request.data.get('unloading_location')).resource.get().pk:
            return Response({'message': 'INVALID_LOCATION'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DriveStartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            drive_route = {
                'drive_record': serializer.instance.pk,
                'longitude': float(serializer.instance.loading_location.longitude),
                'latitude': float(serializer.instance.loading_location.latitude),
                'distance': 0
            }
            drive_route_serializer = DriveRouteSerializer(data=drive_route)
            if drive_route_serializer.is_valid():
                drive_route_serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriveRecordView(APIView, MyPagination):
    @login_required
    def get(self, request, drive_record_id=None):
        try:
            if drive_record_id:
                drive_record = DriveRecord.objects.get(is_active=True, pk=drive_record_id)
                serializer = DriveRecordViewSerializer(drive_record)
                return Response(serializer.data, status=status.HTTP_200_OK)

            admin = request.user
            serializer_class = DriveRecordViewSerializer
            self.pagination_class.page_size = request.GET.get('limit', 10)
            if admin.type == 'ProjectTotalAdmin':
                queryset = DriveRecord.objects.filter(is_active=True, car__site__project__project_admin__pk=admin.pk)
            else:
                queryset = DriveRecord.objects.filter(is_active=True, car__site__site_admin__pk=admin.pk)
            page = self.paginate_queryset(queryset)
            serializer = serializer_class(page, many=True)
            return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                             'result': serializer.data}, status=status.HTTP_200_OK)
        except DriveRecord.DoesNotExist:
            return Response({'message': 'DRIVE_RECORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)


class DriveEndView(APIView):
    @login_required
    def post(self, request):
        if request.data.get('drive_record_id') is None:
            return Response({'message': 'RECORD_NOT_FOUND'}, status=status.HTTP_400_BAD_REQUEST)
        drive_record = DriveRecord.objects.get(pk=request.data['drive_record_id'])
        request.data['total_distance'] = drive_record.driveroute_set.filter(is_active=True).aggregate(total_distance=Sum('distance'))['total_distance']
        serializer = DriveEndSerializer(instance=drive_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgressView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        if admin.type == 'ProjectTotalAdmin':
            sites = Site.objects.filter(is_active=True, project__project_admin__pk=admin.pk)
        else:
            sites = Site.objects.filter(is_active=True, site_admin__pk=admin.pk)

        serializer = ProgressSerializer(sites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DriveRouteView(APIView):
    @login_required
    def post(self, request):
        try:
            if request.data.get('drive_record') is None:
                return Response({'message': 'CHECK_DRIVE_ROUTE_ID'}, status=status.HTTP_400_BAD_REQUEST)
            drive_route = DriveRecord.objects.get(pk=request.data['drive_record']).driveroute_set.first()
            if drive_route is None:
                return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
            float_formatter = "{0:.4f}"
            request.data['distance'] = haversine(
                (drive_route.longitude, drive_route.latitude),
                (request.data['longitude'], request.data['latitude']), unit='km')
            request.data['distance'] = float_formatter.format(request.data['distance'])
            serializer = DriveRouteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DriveRoute.DoesNotExist:
            return Response({'message': 'DRIVE_ROUTE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def get(self, request):
        queryset = DriveRecord.objects.filter(is_active=True,
                                              loading_location__site__project__project_admin__pk=request.user.pk)
        serializer = DriveRouteViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
