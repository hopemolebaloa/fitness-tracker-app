# activities/serializers.py
from rest_framework import serializers
from .models import Activity, ActivityType

class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for the ActivityType model"""
    class Meta:
        model = ActivityType
        fields = ('id', 'name', 'description')

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for the Activity model"""
    activity_type_name = serializers.ReadOnlyField(source='activity_type.name')
    
    class Meta:
        model = Activity
        fields = ('id', 'activity_type', 'activity_type_name', 'duration', 'distance', 
                 'distance_unit', 'calories_burned', 'date', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def create(self, validated_data):
        # Set the user to the current authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity summary metrics"""
    total_duration = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_calories = serializers.IntegerField()
    total_activities = serializers.IntegerField()
    timeframe = serializers.CharField()