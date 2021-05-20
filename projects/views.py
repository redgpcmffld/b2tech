from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ResourceSerializer,
    ResourceViewSerializer
)

from .models import Resource


class ResourceListView(APIView):
    def get(self, request):
        return Response(Resource.TYPES)


class ResourceView(APIView):
    def post(self, request):
        try:
            serializer = ResourceSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({'message': Exception}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            resources = Resource.objects.filter(is_active=True)
            serializer = ResourceViewSerializer(resources, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Resource.DoesNotExist:
            return Response({'message': 'DATA_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            if Resource.objects.filter(pk=request.data['resource_id']).exists():
                resource = Resource.objects.get(pk=request.data['resource_id'])

            serializer = ResourceSerializer(resource, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resource_id):
        try:
            resource = Resource.objects.get(pk=resource_id, is_active=True)
            resource.is_active = False
            resource.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

        except Resource.DoesNotExist:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)
