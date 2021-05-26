from django.http import JsonResponse
from django.views import View

from ..models.drive_record import DriveRecord

from utils import login_required


class GraphView(View):
    @login_required
    def get(self, request):
        admin = request.user

        result = [{
            'type': drive.unloading_location.resource.get().type
        } for drive in DriveRecord.objects.filter(is_active=True, status__in=[2, 4],
                                                  car__site__project__project_admin__pk=admin.pk)]

        return JsonResponse({'result': result}, status=200)
