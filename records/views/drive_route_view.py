from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.drive_record import DriveRecord
from ..models.drive_route import DriveRouteSerializer, DriveRouteViewSerializer

from utils import login_required


class DriveRouteView(APIView):
    @login_required
    def post(self, request):
        serializer = DriveRouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def get(self, request):
        q = Q(is_active=True)
        q.add(Q(loading_location__site__project__project_admin__pk=request.user.pk), q.AND)
        if site_id := request.GET.get('site_id'):
            q.add(Q(loading_location__site__pk=site_id), q.AND)
        queryset = DriveRecord.objects.filter(q)
        serializer = DriveRouteViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
