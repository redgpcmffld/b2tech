from django.views import View
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils import login_required
from pagination import MyPagination
from .models import Resource, Car, Location, Site, Project
from .serializers import (
    ResourceSerializer,
    ResourceViewSerializer,
    CarSerializer,
    CarViewSerializer,
    SiteSerializer,
    SiteViewSerializer,
    LocationSerializer,
    LocationViewSerializer,
)


class ProjectSiteView(View):
    @login_required
    def get(self, request):
        admin = request.user
        if admin.type == 'ProjectTotalAdmin':

            data = [{
                'project_id': project.pk,
                'name': project.name,
                'site': [{
                    'site_id': site.pk,
                    'name': site.name
                } for site in project.site_set.all()]
            } for project in Project.objects.filter(is_active=True, project_admin__pk=admin.pk)]

            return JsonResponse({'result': data}, status=200)

        if admin.type == 'SiteAdmin':

            data = [{
                'project': {
                    'project_id': site.project.pk,
                    'name': site.project.name
                },
                'site_id': site.pk,
                'name' : site.name,
            } for site in Site.objects.filter(is_active=True, site_admin__pk=admin.pk)]

            return JsonResponse({'result': data}, status=200)


class ResourceTypeView(APIView):
    @login_required
    def get(self, request):
        return Response(Resource.TYPES)


class ResourceView(APIView, MyPagination):
    @login_required
    def get(self, request):
        admin = request.user

        if admin.type == 'ProjectTotalAdmin':
            queryset = Resource.objects.filter(is_active=True, location__site__project__project_admin__pk=admin.pk)
        else:
            queryset = Resource.objects.filter(is_active=True, location__site__site_admin__pk=admin.pk)

        self.pagination_class.page_size = request.GET.get('limit', 10)
        page = self.paginate_queryset(queryset)
        serializer = ResourceViewSerializer(page, many=True)

        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            serializer = ResourceSerializer(data=request.data)

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
            serializer = ResourceSerializer(resource, data=request.data)

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
            serializer = CarSerializer(data=request.data)

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

            serializer = CarSerializer(car, data=request.data)

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
        return Response({'last_page': queryset.count() // int(self.pagination_class.page_size),
                         'result': serializer.data}, status=status.HTTP_200_OK)

    @login_required
    def post(self, request):
        try:
            if request.data['start_date'] > request.data['end_date']:
                return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

            if Site.objects.filter(name=request.data['name']).exists():
                return Response({'message': 'DUPLICATE_NAME'}, status=status.HTTP_409_CONFLICT)

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
