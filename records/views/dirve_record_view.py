from datetime import date

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.drive_record import (
    DriveRecord,
    DriveRecordViewSerializer,
    DriveRecordCreateSerializer,
    DriveRecordUpdateSerializer
)
from ..models.drive_route import DriveRouteCreateSerializer, DriveRouteViewSerializer

from utils import login_required
from pagination import MyPagination


class DriveRecordView(APIView, MyPagination):
    @login_required
    def post(self, request, drive_record_id=None):
        try:
            admin = request.user
            if drive_record_id is None:
                car_pk = request.data['car']
                serializer = DriveRecordCreateSerializer(data=request.data, context={'admin': admin, 'car_pk': car_pk})
                if serializer.is_valid():
                    serializer.save()
                    drive_route = {
                        'drive_record': serializer.instance.pk,
                        'longitude': float(serializer.instance.loading_location.longitude),
                        'latitude': float(serializer.instance.loading_location.latitude)
                    }
                    drive_route_serializer = DriveRouteCreateSerializer(data=drive_route)
                    if drive_route_serializer.is_valid():
                        drive_route_serializer.save()
                        return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            drive_record = DriveRecord.objects.get(pk=drive_record_id)
            serializer = DriveRecordUpdateSerializer(instance=drive_record, data=request.data)
            if serializer.is_valid():
                drive_route = {
                    'drive_record': serializer.instance.pk,
                    'longitude': float(serializer.instance.unloading_location.longitude),
                    'latitude': float(serializer.instance.unloading_location.latitude)
                }
                drive_route_serializer = DriveRouteCreateSerializer(data=drive_route)
                if drive_route_serializer.is_valid():
                    drive_route_serializer.save()
                    serializer.save()
                    return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'KEY_ERROR'}, status=status.HTTP_400_BAD_REQUEST)
        except DriveRecord.DoesNotExist:
            return Response({'message': 'INVALID_LOCATION'}, status=status.HTTP_400_BAD_REQUEST)

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
            q = Q(is_active=True)

            if request.GET.get('today'):
                q.add(Q(driving_date=date.today()), q.AND)

            if admin.type == 'ProjectTotalAdmin':
                q.add(Q(car__site__project__project_admin__pk=admin.pk), q.AND)
            else:
                q.add(Q(car__site__site_admin__pk=admin.pk), q.AND)

            queryset = DriveRecord.objects.filter(q)
            page = self.paginate_queryset(queryset)
            serializer = serializer_class(page, many=True)
            return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                             'result': serializer.data}, status=status.HTTP_200_OK)
        except DriveRecord.DoesNotExist:
            return Response({'message': 'DRIVE_RECORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)


class DriveRecordDetailView(APIView):

    @login_required
    def post(self, request, drive_record_id):
        request.data['drive_record'] = drive_record_id
        serializer = DriveRouteCreateSerializer(data=request.data, context={'admin': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def get(self, request, drive_record_id=None):
        try:
            q = Q(is_active=True)
            if request.user.type == 'ProjectTotalAdmin':
                q.add(Q(loading_location__site__project__project_admin__pk=request.user.pk), q.AND)
            elif request.user.type == 'SiteAdmin':
                q.add(Q(loading_location__site__site_admin__pk=request.user.pk), q.AND)
            if site_id := request.GET.get('site_id'):
                q.add(Q(loading_location__site__pk=site_id), q.AND)
            if drive_record_id is None:
                queryset = DriveRecord.objects.filter(q)
                serializer = DriveRouteViewSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            queryset = DriveRecord.objects.get(q, pk=drive_record_id)
            serializer = DriveRouteViewSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DriveRecord.DoesNotExist:
            return Response({'message': 'DRIVE_RECORD_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
