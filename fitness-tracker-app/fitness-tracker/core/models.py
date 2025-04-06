from django.db import models
from django.conf import settings
from activities.models import ActivityType

class Goal(models.Model):
    """Model for storing user fitness goals"""
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    
    METRIC_CHOICES = (
        ('duration', 'Duration'),
        ('distance', 'Distance'),
        ('calories', 'Calories'),
        ('sessions', 'Number of Sessions'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, related_name='goals', blank=True, null=True)
    target_value = models.FloatField()
    metric = models.CharField(max_length=10, choices=METRIC_CHOICES)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"