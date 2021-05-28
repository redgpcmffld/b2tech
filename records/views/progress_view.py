from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from projects.models.site import Site
from ..models.progress import ProgressViewSerializer

from utils import login_required


class ProgressView(APIView):
    @login_required
    def get(self, request):
        admin = request.user
        if admin.type == 'ProjectTotalAdmin':
            sites = Site.objects.filter(is_active=True, project__project_admin__pk=admin.pk)
        else:
            sites = Site.objects.filter(is_active=True, site_admin__pk=admin.pk)

        serializer = ProgressViewSerializer(sites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
