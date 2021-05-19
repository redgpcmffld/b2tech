from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CarSerializer,
    CarSerializerGet
)

from .models import Car


class CarListView(APIView):
    def get(self, request):
        return Response(Car.TYPES)


class CarView(APIView):
    def post(self, request):
        try:
            if Car.objects.filter(number=request.data['number']):
                return Response({'message': 'NUMBER_EXIST'}, status=status.HTTP_409_CONFLICT)

            serializer = CarSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response(Exception.error, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            cars = Car.objects.filter(is_active=True)
            serializer = CarSerializerGet(cars, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Car.DoesNotExist:
            return Response({'message': 'DATA_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            if Car.objects.filter(pk=request.data['car_id']).exists():
                car = Car.objects.get(pk=request.data['car_id'])

            serializer = CarSerializer(car, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, car_id):
        try:
            car = Car.objects.get(pk=car_id, is_active=True)
            car.is_active = False
            car.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

        except Car.DoesNotExist:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)
