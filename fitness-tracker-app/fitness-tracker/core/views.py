from rest_framework import viewsets, permissions
from .models import Goal
from .serializers import GoalSerializer
from activities.views import IsOwnerOrReadOnly

class GoalViewSet(viewsets.ModelViewSet):
    """API endpoint for managing user goals"""
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    
    def get_queryset(self):
        """
        This view returns a list of all goals
        for the currently authenticated user.
        """
        user = self.request.user
        return Goal.objects.filter(user=user)