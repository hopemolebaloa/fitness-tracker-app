from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    """Serializer for the Goal model"""
    activity_type_name = serializers.ReadOnlyField(source='activity_type.name')
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = ('id', 'title', 'activity_type', 'activity_type_name', 
                 'target_value', 'metric', 'period', 'start_date', 
                 'end_date', 'is_completed', 'progress', 'created_at')
        read_only_fields = ('id', 'is_completed', 'progress', 'created_at')
    
    def create(self, validated_data):
        # Set the user to the current authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_progress(self, obj):
        """Calculate the progress towards the goal"""
        # To be implemented based on user's activities
        # This is a placeholder
        return 0.0