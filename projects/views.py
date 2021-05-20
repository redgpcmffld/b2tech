from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializers import LocationSerializer, LocationViewSerializer
from .models import Location, Site
from pagination import MyPagination


class LocationView(APIView, MyPagination):
    def get(self, request):
        try:
            self.queryset = Location.objects.filter(is_active=True)
            self.serializer_class = LocationViewSerializer
            PageNumberPagination.page_size = request.GET.get('limit', 10)
            self.pagination_class = PageNumberPagination
            page = self.paginate_queryset(self.queryset)
            serializer = self.serializer_class(page, many=True)
            return Response({'last_page': self.queryset.count()//int(self.pagination_class.page_size),
                             'count': self.queryset.count(),
                             'result': serializer.data}, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({'message': '존재하지 않는 지역 입니다.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            if Location.objects.filter(
                    name=request.data.get('name'),
                    type=request.data.get('type'),
                    site_id=request.data.get('site')).exists():
                return Response({'message': '이미 등록되어 있는 지역입니다.'}, status=status.HTTP_409_CONFLICT)
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': Exception}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            if request.data.get('location_id') is None:
                return Response({'message': '지역 정보를 입력해주세요'}, status=status.HTTP_400_BAD_REQUEST)

            location = Location.objects.get(pk=request.data.get('location_id'))
            serializer = LocationSerializer(location, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({'message': '존재하지 않는 지역 정보 입니다.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, location_id):
        try:
            location = Location.objects.get(pk=location_id, is_active=True)
            location.is_active = False
            location.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({'message': '존재하지 않는 지역 정보 입니다.'}, status=status.HTTP_404_NOT_FOUND)
