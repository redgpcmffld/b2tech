from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from haversine import haversine

from ..models.drive_record import DriveRecord
from ..models.drive_route import DriveRoute, DriveRouteSerializer, DriveRouteViewSerializer

from utils import login_required


class DriveRouteView(APIView):
    @login_required
    def post(self, request):
        try:
            if request.data.get('drive_record') is None:
                return Response({'message': 'CHECK_DRIVE_ROUTE_ID'}, status=status.HTTP_400_BAD_REQUEST)
            drive_route = DriveRecord.objects.get(pk=request.data['drive_record']).driveroute_set.first()
            if drive_route is None:
                return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)
            float_formatter = "{0:.4f}"
            request.data['distance'] = haversine(
                (drive_route.longitude, drive_route.latitude),
                (request.data['longitude'], request.data['latitude']), unit='km')
            request.data['distance'] = float_formatter.format(request.data['distance'])
            serializer = DriveRouteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'CREATE_SUCCESS'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DriveRoute.DoesNotExist:
            return Response({'message': 'DRIVE_ROUTE_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'message': 'BAD_REQUEST'}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def get(self, request):
        queryset = DriveRecord.objects.filter(is_active=True,
                                              loading_location__site__project__project_admin__pk=request.user.pk)
        serializer = DriveRouteViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
