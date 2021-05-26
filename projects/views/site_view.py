from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.site import Site, SiteSerializer, SiteViewSerializer

from utils import login_required
from pagination import MyPagination


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
                return Response({'message': 'INVALID_DATE'}, status=status.HTTP_400_BAD_REQUEST)

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
