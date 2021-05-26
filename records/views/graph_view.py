from django.http import JsonResponse
from django.views import View

from ..models.drive_record import DriveRecord

from utils import login_required


class GraphView(View):
    @login_required
    def get(self, request):
        admin = request.user

        drive = DriveRecord.objects.filter(is_active=True, status__in=[2, 4],
                                           car__site__project__project_admin__pk=admin.pk,
                                           unloading_location__resource__type='Iron')

        month_list = []
        for month in drive:
            if month.driving_date.month == 5:
                month_list.append(month.driving_date.month)

        return JsonResponse({'Iron': len(month_list)}, status=200)
