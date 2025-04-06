f# activities/serializers.py
from rest_framework import serializers
from .models import Activity, ActivityType

class ActivityTypeSerializer(serializers.ModelSerializer):
    """Serializer for activity types"""
    class Meta:
        model = ActivityType
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for activities"""
    activity_type_name = serializers.ReadOnlyField(source='activity_type.name')
    
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'activity_type_name', 'duration', 'distance', 
                 'calories_burned', 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']