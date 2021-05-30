import math

from django.db.models import Q, Func, F, Value, CharField
from django.http import HttpResponse

from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.site import Site, SiteCreateSerializer, SiteViewSerializer

from utils import login_required
from pagination import MyPagination


class SiteView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user

        if admin.type == 'ProjectTotalAdmin':
            queryset = Site.objects.filter(is_active=True, project__project_admin__pk=admin.pk)
        else:
            queryset = Site.objects.filter(is_active=True, site_admin__pk=admin.pk)

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = SiteViewSerializer(page, many=True)
        return Response({'last_page': math.ceil(queryset.count() / int(self.pagination_class.page_size)),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            if request.data['start_date'] > request.data['end_date']:
                return Response({'message': 'INVALID_DATE'}, status=status.HTTP_400_BAD_REQUEST)

            if Site.objects.filter(name=request.data['name']).exists():
                return Response({'message': 'DUPLICATE_NAME'}, status=status.HTTP_409_CONFLICT)

            serializer = SiteCreateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        try:
            if request.data.get('site_id') is None:
                return Response({'message': 'CHECK_SITE_ID'}, status=status.HTTP_400_BAD_REQUEST)

            site = Site.objects.get(pk=request.data['site_id'])
            serializer = SiteCreateSerializer(site, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Site.DoesNotExist:
            return Response({'message': 'SITE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    def delete(self, request, site_id):
        try:
            site = Site.objects.get(pk=site_id, is_active=True)
            site.is_active = False
            site.save()
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)

        except Site.DoesNotExist:
            return Response({'message': 'SITE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)


class SiteListExportView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site_admin__pk=admin.pk), q.AND)

        queryset = Site.objects.filter(q)
        excel_data = []
        excel_data.append(('id', '프로젝트명', '현장명', '시작연도', '시작월', '종료연도', '종료월'))
        sites = queryset.annotate(
            start=Func(F('start_date'), Value('%Y-%m'), function='DATE_FORMAT', output_field=CharField()),
            end=Func(F('end_date'), Value('%Y-%m'), function='DATE_FORMAT', output_field=CharField())
        ).values_list(
            'pk',
            'project__name',
            'name',
            'start',
            'end'
        )
        for site in sites:
            excel_data.append(
                list(site)
            )
        if excel_data:
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()
            for line in excel_data:
                ws.append(line)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=site_list.xlsx'

        wb.save(response)
        return response
