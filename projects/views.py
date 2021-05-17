import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Site


class SiteView(View):
    def post(self, request):
        data = json.loads(request.body)

        project = data.get('project')
        name = data.get('name')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        admin = data.get('admin')

        if not project or not name or not start_date or not end_date or not admin:
            return JsonResponse({'message': 'CHECK_YOUR_INPUT'}, status=200)

        if Site.objects.filter(name=name).exists():
            return JsonResponse({'message': 'NAME_EXIST'}, status=409)

        Site(project=project, name=name, start_date=start_date, end_date=end_date, admin=admin).save()

        return HttpResponse(status=200)