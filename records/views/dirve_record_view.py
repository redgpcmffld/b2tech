from datetime import date

from django.db.models import Sum, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.drive_record import DriveRecord, DriveRecordViewSerializer, DriveEndSerializer, DriveStartSerializer
from ..models.drive_route import DriveRouteSerializer
from projects.models.location import Location

from utils import login_required
from pagination import MyPagination


class DriveStartView(APIView):
    @login_required
    def post(self, request):
        try:
            admin = request.user
            car_pk = request.data['car']
            serializer = DriveStartSerializer(data=request.data, context={'admin': admin, 'car_pk': car_pk})
            if serializer.is_valid():
                serializer.save()
                drive_route = {
                    'drive_record': serializer.instance.pk,
                    'longitude': float(serializer.instance.loading_location.longitude),
                    'latitude': float(serializer.instance.loading_location.latitude)
                }
                drive_route_serializer = DriveRouteSerializer(data=drive_route)
                if drive_route_serializer.is_valid():
                    drive_route_serializer.save()
                    return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'KEY_ERROR'}, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({'message': 'INVALID_LOCATION'}, status=status.HTTP_400_BAD_REQUEST)


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
            q = Q(is_active=True)
            if request.GET.get('today'):
                q.add(Q(driving_date=date.today()), q.AND)
            if admin.type == 'ProjectTotalAdmin':
                q.add(Q(car__site__project__project_admin__pk=admin.pk), q.AND)
                queryset = DriveRecord.objects.filter(q)
            else:
                q.add(Q(car__site__site_admin__pk=admin.pk), q.AND)
                queryset = DriveRecord.objects.filter(q)
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
        request.data['total_distance'] = \
            drive_record.driveroute_set.filter(is_active=True).aggregate(total_distance=Sum('distance'))[
                'total_distance']
        serializer = DriveEndSerializer(instance=drive_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            drive_route = {
                'drive_record': serializer.instance.pk,
                'longitude': float(serializer.instance.loading_location.longitude),
                'latitude': float(serializer.instance.loading_location.latitude)
            }
            drive_route_serializer = DriveRouteSerializer(data=drive_route)
            if drive_route_serializer.is_valid():
                drive_route_serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
