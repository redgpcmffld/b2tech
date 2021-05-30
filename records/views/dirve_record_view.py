from datetime import date

from django.db.models import Q, Case, When, Value
from django.http import HttpResponse

from openpyxl import Workbook
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
                driver_pk = request.data['driver']
                serializer = DriveRecordCreateSerializer(
                    data=request.data, context={'admin': admin, 'car_pk': car_pk, 'driver_pk': driver_pk}
                )
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

            if site := request.GET.get('site'):
                q.add(Q(car__site__pk=site), q.AND)

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


class DriveRecordListExportView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(loading_location__site__project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(loading_location__site__site_admin__pk=admin.pk), q.AND)

        queryset = DriveRecord.objects.filter(q)
        excel_data = []
        excel_data.append(('id', '차량번호', '기사이름', '상차지', '하차지', '출발시간', '도착시간', '총거리', '상태', '성상 이름', '성상 무게', '성상 단위'))
        drive_records = queryset.annotate(
            resource_block=Case(
                When(loading_location__resource__block='m**3', then=Value(u'm\u00B3')),
                When(~Q(loading_location__resource__block='m**3'), then='loading_location__resource__block'),
            ),
            drive_status = Case(
                When(status=1, then=Value('상차')),
                When(status=2, then=Value('정상종료')),
                When(status=3, then=Value('강제하차승인요청')),
                When(status=4, then=Value('강제하차확인'))
            )
        ).values_list(
            'pk',
            'car__number',
            'driver__name',
            'loading_location__name',
            'unloading_location__name',
            'loading_time',
            'unloading_time',
            'total_distance',
            'drive_status',
            'loading_location__resource__name',
            'transport_weight',
            'resource_block'
        ).distinct()
        for drive_record in drive_records:
            excel_data.append(
                list(drive_record)
            )
        if excel_data:
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()
            for line in excel_data:
                ws.append(line)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=drive_record_list.xlsx'

        wb.save(response)
        return response
