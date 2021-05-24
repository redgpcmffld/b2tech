from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils import login_required
from pagination import MyPagination
from .models import Car, Location, Site
from .serializers import CarSerializer, CarViewSerializer, SiteSerializer, SiteViewSerializer, LocationSerializer, \
    LocationViewSerializer


class CarTypeView(APIView):
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
            return Response({'message': Exception}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            cars = Car.objects.filter(is_active=True)
            serializer = CarViewSerializer(cars, many=True)

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


class SiteView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user

        if admin.type == 'ProjectTotalAdmin':
            queryset = Site.objects.filter(is_active=True, project__project_admin__pk=admin.pk)
        else:
            queryset = Site.objects.filter(is_active=True, Site_admin__pk=admin.pk)

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = SiteViewSerializer(page, many=True)
        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            request.data['start_date'] = f"{request.data['start_date']}-01"
            request.data['end_date'] = f"{request.data['end_date']}-01"

            serializer = SiteSerializer(data=request.data)

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
            serializer = SiteSerializer(site, data=request.data)

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
