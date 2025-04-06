# activities/views.py
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Activity, ActivityType
from .serializers import ActivitySerializer, ActivityTypeSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on activities"""
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'date']
    ordering_fields = ['date', 'duration', 'calories_burned']
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityTypeListView(generics.ListAPIView):
    """View for listing activity types"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_metrics(request):
    """Get metrics for user activities"""
    user = request.user
    
    # Default to last 30 days if no date range provided
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get query parameters for date range
    start_date_param = request.query_params.get('start_date')
    end_date_param = request.query_params.get('end_date')
    
    if start_date_param:
        start_date = timezone.datetime.strptime(start_date_param, '%Y-%m-%d').date()
    if end_date_param:
        end_date = timezone.datetime.strptime(end_date_param, '%Y-%m-%d').date()
    
    # Get activities in date range
    activities = Activity.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    )
    
    # Calculate metrics
    total_activities = activities.count()
    total_duration = activities.aggregate(Sum('duration'))['duration__sum'] or 0
    total_distance = activities.aggregate(Sum('distance'))['distance__sum'] or 0
    total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    
    # Activity breakdown by type
    activity_breakdown = activities.values('activity_type__name').annotate(
        count=Count('id'),
        total_duration=Sum('duration'),
        total_distance=Sum('distance'),
        total_calories=Sum('calories_burned')
    )
    
    return Response({
        'period': {
            'start_date': start_date,
            'end_date': end_date,
        },
        'summary': {
            'total_activities': total_activities,
            'total_duration': total_duration,
            'total_distance': total_distance,
            'total_calories': total_calories,
        },
        'activity_breakdown': activity_breakdown
    })