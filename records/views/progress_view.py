from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.site import Site
from ..models.progress import ProgressSerializer, WorkLoadSerializer

from utils import login_required


class ProgressView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site_admin__pk=admin.pk), q.AND)

        sites = Site.objects.filter(q)

        serializer = ProgressSerializer(sites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkLoadsView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        q = Q(is_active=True)
        if admin.type == 'ProjectTotalAdmin':
            q.add(Q(project__project_admin__pk=admin.pk), q.AND)
        else:
            q.add(Q(site_admin__pk=admin.pk), q.AND)

        if site := request.GET.get('site'):
            q.add(Q(pk=site), q.AND)

        sites = Site.objects.filter(q)

        serializer = WorkLoadSerializer(sites)

        return Response(serializer.data, status=status.HTTP_200_OK)
