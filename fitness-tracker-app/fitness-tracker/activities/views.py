# activities/views.py
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta
from .models import Activity, ActivityType
from .serializers import ActivitySerializer, ActivityTypeSerializer, ActivitySummarySerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it"""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the activity
        return obj.user == request.user

class ActivityTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for activity types"""
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ActivityViewSet(viewsets.ModelViewSet):
    """API endpoint for managing user activities"""
    serializer_class = ActivitySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['activity_type__name', 'notes']
    ordering_fields = ['date', 'duration', 'calories_burned']
    
    def get_queryset(self):
        """
        This view returns a list of all activities
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Activity.objects.filter(user=user)
        
        # Filter by date range if provided in query params
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if activity_type:
            queryset = queryset.filter(activity_type__id=activity_type)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns a summary of user activities.
        """
        user = request.user
        timeframe = request.query_params.get('timeframe', 'week')
        
        # Set date range based on timeframe
        today = timezone.now().date()
        if timeframe == 'week':
            start_date = today - timedelta(days=7)
        elif timeframe == 'month':
            start_date = today - timedelta(days=30)
        elif timeframe == 'year':
            start_date = today - timedelta(days=365)
        else:  # all time
            start_date = None
        
        # Filter activities by date range
        activities = Activity.objects.filter(user=user)
        if start_date:
            activities = activities.filter(date__gte=start_date)
        
        # Calculate summary metrics
        summary = {
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_calories': activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'total_activities': activities.count(),
            'timeframe': timeframe
        }
        
        serializer = ActivitySummarySerializer(summary)
        return Response(serializer.data)