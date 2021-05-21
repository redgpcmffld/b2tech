from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Site
from .serializers import SiteSerializer, SiteViewSerializer


class SiteView(APIView):
    def post(self, request):
        try:
            if Site.objects.filter(name=request.data['name']).exists():
                return Response({'message': 'NAME_EXIST'}, status=status.HTTP_409_CONFLICT)

            serializer = SiteSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({'message': Exception}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            sites = Site.objects.filter(is_active=True)
            serializer = SiteViewSerializer(sites, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Site.DoesNotExist:
            return Response({'message': 'DATA_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            if Site.objects.filter(pk=request.data['site_id']).exists():
                site = Site.objects.get(pk=request.data['site_id'])

            serializer = SiteSerializer(site, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, site_id):
        try:
            site = Site.objects.get(pk=site_id, is_active=True)
            site.is_active = False
            site.save()
            return Response({'message': 'SUCCESS'}, status=status.HTTP_200_OK)

        except Site.DoesNotExist:
            return Response({'message': 'CHECK_YOUR_INPUT'}, status=status.HTTP_400_BAD_REQUEST)
