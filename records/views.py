from django.db.models import Sum, Max

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DriveRecord, DriveRoute
from projects.models import Project, Site
from .serializers import DriveStartSerializer, DriveRecordViewSerializer, DriveEndSerializer, ProgressSerializer
from utils import login_required
from pagination import MyPagination


class DriveStartView(APIView):
    @login_required
    def post(self, request):
        serializer = DriveStartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
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
