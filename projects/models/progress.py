from datetime import date

from django.db.models import Sum, Max, Min, Q, Count, Case, When

from rest_framework import serializers

from projects.models.sites import Site


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

    def get_progress(self, site):
        site_max_plan = self.instance.annotate(site_plan=Sum('location__plan')).aggregate(Max('site_plan'))[
            'site_plan__max']
        plan = site.location_set.aggregate(Sum('plan'))['plan__sum']
        site_plan = int(plan / site_max_plan * 5)
        today_workloads = site.location_set.filter(is_active=True).aggregate(
            today_workloads=Sum('loading_location__transport_weight',
                                filter=Q(loading_location__driving_date=date.today()) & Q(loading_location__status=2)))[
            'today_workloads']
        days = (site.end_date - site.start_date).days
        today_plan = plan // days
        if today_workloads is None:
            today_workloads = 0
        progress = int(today_workloads / today_plan * 5)
        if progress == 0:
            progress = 1
        elif progress >= 5:
            progress = 5
        if site_plan == 0:
            site_plan = 1
        elif site_plan >= 5:
            site_plan = 5
        result = {
            'weight': site_plan,
            'percent': progress
        }

        return result

    def get_site_coordinate(self, site):
        site_coordinates = site.location_set.filter(is_active=True).aggregate(Min('longitude'), Max('longitude'),
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

    def get_site_name(self, site):
        return site.name


class WorkLoadSerializer(serializers.Serializer):
    this_week_workloads = serializers.SerializerMethodField(method_name='get_this_week_workloads')
    this_month_workloads = serializers.SerializerMethodField(method_name='get_this_month_workloads')
    this_year_workloads = serializers.SerializerMethodField(method_name='get_this_year_workloads')
    detail_workloads = serializers.SerializerMethodField(method_name='get_detail_workloads')

    class Meta:
        model = Site
        fields = [
            'this_week_workloads',
            'this_month_workloads',
            'this_year_workloads',
            'detail_workloads'
        ]

    def get_this_week_workloads(self, sites):
        q = Q(location__loading_location__driving_date__week=date.today().isocalendar()[1])
        this_week_workloads = sites.aggregate(
            this_week_workloads=Count('location__loading_location', filter=q))['this_week_workloads']
        return this_week_workloads

    def get_this_month_workloads(self, sites):
        q = Q(location__loading_location__driving_date__month=date.today().month)
        this_month_workloads = sites.aggregate(
            this_month_workloads=Count('location__loading_location', filter=q))['this_month_workloads']
        return this_month_workloads

    def get_this_year_workloads(self, sites):
        q = Q(location__loading_location__driving_date__year=date.today().year)
        this_year_workloads = sites.aggregate(
            this_year_workloads=Count('location__loading_location', filter=q))['this_year_workloads']
        return this_year_workloads

    def get_detail_workloads(self, sites):

        month = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        types = ('Iron', 'Dirt', 'Stone', 'Waste')
        results = []
        for m in month:
            q1 = Q(location__loading_location__driving_date__month=m)
            result = {}
            for type in types:
                q2 = Q(location__resource__type=type)
                workloads = sites.aggregate(workloads=Count('location__loading_location', filter=q1 & q2))
                result[f'{type}'] = workloads['workloads']
            results.append(result)

        return results
