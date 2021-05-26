from datetime import date

from django.db.models import Sum, Max, Min, Q

from rest_framework import serializers

from projects.models.site import Site


class ProgressSerializer(serializers.Serializer):
    site_id = serializers.IntegerField(read_only=True)
    site_name = serializers.SerializerMethodField(method_name='get_site_name')
    progress = serializers.SerializerMethodField(method_name='get_progress')
    site_coordinate = serializers.SerializerMethodField(method_name='get_site_coordinate')

    class Meta:
        model = Site
        fields = [
            'site_id',
            'site_name',
            'percent',
            'weight',
            'site_coordinate'
        ]

    def get_progress(self, obj):
        site_max_plan = self.instance.annotate(site_plan=Sum('location__plan')).aggregate(Max('site_plan'))[
            'site_plan__max']
        plan = obj.location_set.aggregate(Sum('plan'))['plan__sum']
        site_plan = int(plan / site_max_plan * 5)
        today_workloads = obj.location_set.filter(is_active=True).aggregate(
            today_workloads=Sum('loading_location__transport_weight',
                                filter=Q(loading_location__driving_date=date.today()) & Q(loading_location__status=2)))[
            'today_workloads']
        days = (date.fromisoformat(obj.end_date) - date.fromisoformat(obj.start_date)).days
        today_plan = plan // days
        if today_workloads is None:
            today_workloads = 0
        progress = int(today_workloads / today_plan * 5)
        if progress == 0:
            progress = 1
        if site_plan == 0:
            site_plan = 1
        result = {
            'weight': site_plan,
            'percent': progress
        }

        return result

    def get_site_coordinate(self, obj):
        site_coordinates = obj.location_set.filter(is_active=True).aggregate(Min('longitude'), Max('longitude'),
                                                                             Min('latitude'), Max('latitude'))
        if site_coordinates['longitude__min'] and \
                site_coordinates['longitude__max'] and \
                site_coordinates['latitude__min'] and \
                site_coordinates['latitude__max'] is None:
            return {'longitude': 0, 'latitude': 0}
        result = {
            'longitude': (site_coordinates['longitude__min'] +
                          (site_coordinates['longitude__max'] - site_coordinates['longitude__min'])
                          // 2),
            'latitude': (site_coordinates['latitude__min'] +
                         (site_coordinates['latitude__max'] - site_coordinates['latitude__min'])
                         // 2)
        }
        return result

    def get_site_name(self, obj):
        return obj.name
