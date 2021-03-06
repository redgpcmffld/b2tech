from django.views import View
from django.http import JsonResponse

from projects.models.projects import Project
from projects.models.sites import Site

from utils import login_required


class ProjectSiteView(View):
    @login_required
    def get(self, request):
        admin = request.user

        if admin.type == 'ProjectTotalAdmin':
            data = [{
                'project_id': project.pk,
                'name': project.name,
                'site': [{
                    'site_id': site.pk,
                    'name': site.name
                } for site in project.site_set.filter(is_active=True)]
            } for project in Project.objects.filter(is_active=True, project_admin__pk=admin.pk)]

            return JsonResponse({'result': data}, status=200)

        if admin.type == 'SiteAdmin':
            data = [{
                'project_id': site.project.pk,
                'name': site.project.name,
                'site': {
                    'site_id': site.pk,
                    'name': site.name
                },
            } for site in Site.objects.filter(is_active=True, site_admin__pk=admin.pk)]

            return JsonResponse({'result': data}, status=200)
