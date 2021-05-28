from django.db.models import F
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openpyxl import Workbook

from projects.models.location import Location, LocationSerializer, LocationViewSerializer

from utils import login_required
from pagination import MyPagination


class LocationView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user
        if admin.type == 'ProjectTotalAdmin':
            queryset = Location.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Location.objects.filter(is_active=True, site__site_admin__pk=admin.pk)
        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = LocationViewSerializer(page, many=True)

        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            if Location.objects.filter(
                    name=request.data['name'],
                    type=request.data['type']).exists():
                return Response({'message': 'DUPLICATE_LOCATION'}, status=status.HTTP_409_CONFLICT)
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

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


class LocationExportView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        if admin.type == 'ProjectTotalAdmin':
            queryset = Location.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Location.objects.filter(is_active=True, site__site_admin__pk=admin.pk)

        # Location.objects.filter(site__site_admin__pk=4).values('pk', 'name', 'longitude', 'latitude',
        #                                                        location_type=Case(When(type=1, then=Value('상차지')), When(type=0, then=Value('하차지'))))
        excel_data = []
        excel_data.append(list(queryset.values(site_name=F('site__name'), pk='pk', longitude='longitude', latitude='latitude')))
        for location in Location.objects.values_list():
            excel_data.append(
                list(location)
            )
        if excel_data:
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()
            for line in excel_data:
                ws.append(line)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=mydata.xlsx'

        wb.save(response)
        return response
