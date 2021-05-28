from django.http import JsonResponse
from django.views import View

from ..models.drive_record import DriveRecord

from utils import login_required


class GraphView(View):
    @login_required
    def get(self, request):
        admin = request.user

        if admin.type == 'ProjectTotalAdmin':
            drives = DriveRecord.objects.filter(is_active=True, status__in=[2, 4],
                                                car__site__project__project_admin__pk=admin.pk,
                                                unloading_location__resource__type='Iron').count()

            return JsonResponse({'Iron': drives}, status=200)


# drive_list = []
            # for drive in drives:
            #     if drive.driving_date.month == 5:
            #         drive_list.append(drive.driving_date.month)