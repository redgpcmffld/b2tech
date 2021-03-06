import math

from django.db.models import Q, Case, When, Value
from django.http import HttpResponse

from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.cars import Car
from projects.serializers.cars import CarCreateSerializer, CarViewSerializer

from utils import login_required
from pagination import MyPagination


class CarTypeView(APIView):
    @login_required
    def get(self, request):
        return Response(Car.TYPES)


class CarView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user

        q = Q(is_active=True)

        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(site__project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site__site_admin__pk=admin.pk), q.AND)

        if search := request.GET.get('search'):
            for keyword in search.split(' '):
                q.add(Q(type__icontains=keyword) |
                      Q(number__icontains=keyword) |
                      Q(site__name__icontains=keyword), q.AND)

        queryset = Car.objects.filter(q).distinct()

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = CarViewSerializer(page, many=True)

        return Response({'last_page': math.ceil(queryset.count() / int(self.pagination_class.page_size)),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            serializer = CarCreateSerializer(data=request.data)

            if Car.objects.filter(number=request.data['number']):
                return Response({'message': 'DUPLICATE_NUMBER'}, status=status.HTTP_409_CONFLICT)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def put(self, request):
        try:
            if request.data.get('car_id') is None:
                return Response({'message': 'CHECK_CAR_ID'}, status=status.HTTP_400_BAD_REQUEST)

            car = Car.objects.get(pk=request.data['car_id'])

            serializer = CarCreateSerializer(car, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'UPDATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Car.DoesNotExist:
            return Response({'message': 'CAR_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    @login_required
    def delete(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id, is_active=True)
            car.is_active = False
            car.save()
            return Response({'message': 'DELETE_SUCCESS'}, status=status.HTTP_204_NO_CONTENT)

        except Car.DoesNotExist:
            return Response({'message': 'CAR_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)


class CarListExportView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(site__project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site__site_admin__pk=admin.pk), q.AND)
        queryset = Car.objects.filter(q)
        excel_data = []
        excel_data.append(('id', '?????????', '??????', '??????', '?????? ??????', '?????? ??????'))
        cars = queryset.annotate(
            car_type=Case(
                When(type='DumpTruck', then=Value('?????? ??????')),
                When(type='WasteTruck', then=Value('????????? ??????')),
                When(type='RecyclingTruck', then=Value('????????? ??????')),
                When(type='Tank', then=Value('??????'))
            )
        ).values_list(
            'pk',
            'site__name',
            'car_type',
            'number',
            'driver__name',
            'driver__phone_number',
        )
        for car in cars:
            excel_data.append(
                list(car)
            )
        if excel_data:
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()
            for line in excel_data:
                ws.append(line)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=car_list.xlsx'

        wb.save(response)
        return response
