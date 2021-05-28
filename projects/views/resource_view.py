from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.resource import Resource, ResourceSerializer, ResourceViewSerializer
from projects.models.location import Location

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

        if admin.type == 'ProjectTotalAdmin':
            queryset = Location.objects.filter(is_active=True, site__project__project_admin__pk=admin.pk)
        else:
            queryset = Location.objects.filter(is_active=True, site__site_admin__pk=admin.pk)

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
