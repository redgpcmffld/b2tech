from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.car import Car, CarCreateSerializer, CarViewSerializer

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

        if admin.type == 'ProjectTotalAdmin':
            queryset = Car.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Car.objects.filter(is_active=True, site__site_admin__pk=admin.pk)

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = CarViewSerializer(page, many=True)

        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
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
