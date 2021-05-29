from django.db.models import Q, Case, When, Value
from django.http import HttpResponse

from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.resource import Resource, ResourceCreateSerializer, ResourceViewSerializer
from projects.models.site import Site

from utils import login_required
from pagination import MyPagination


class ResourceBlockView(APIView):
    @login_required
    def get(self, request):
        return Response(Resource.BLOCK_UNITS)


class ResourceTypeView(APIView):
    @login_required
    def get(self, request):
        return Response(Resource.TYPES)


class ResourceView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user

        q = Q(is_active=True)

        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site_admin__pk=admin.pk), q.AND)

        queryset = Site.objects.filter(q)

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = ResourceViewSerializer(page, many=True)

        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            serializer = ResourceCreateSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        try:
            if request.data.get('resource_id') is None:
                return Response({'message': 'CHECK_RESOURCE_ID'}, status=status.HTTP_400_BAD_REQUEST)

            resource = Resource.objects.get(pk=request.data['resource_id'])
            serializer = ResourceCreateSerializer(resource, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Resource.DoesNotExist:
            return Response({'message': 'RESOURCE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    def delete(self, request, resource_id):
        try:
            resource = Resource.objects.get(pk=resource_id, is_active=True)
            resource.is_active = False
            resource.save()
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)

        except Resource.DoesNotExist:
            return Response({'message': 'RESOURCE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)


class ResourceListExportView(APIView):
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
        excel_data.append(('현장명', '이름', '타입', '단위'))
        resources = queryset.annotate(
            resource_type=Case(
                When(location__resource__type='Iron', then=Value('철')),
                When(location__resource__type='Dirt', then=Value('사토')),
                When(location__resource__type='Stone', then=Value('바위')),
                When(location__resource__type='Waste', then=Value('폐기물'))
                ),
            resource_block=Case(
                When(location__resource__block='m**3', then=Value(u'm\u00B3')),
                When(~Q(location__resource__block='m**3'), then='location__resource__block'),
            )).values_list(
            'name',
            'location__resource__name',
            'resource_type',
            'resource_block'
            ).distinct()

        for resource in resources:
            excel_data.append(
                list(resource)
            )
        if excel_data:
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()
            for line in excel_data:
                ws.append(line)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=resource_list.xlsx'

        wb.save(response)
        return response
