from django.db import models
from django.conf import settings

class ActivityType(models.Model):
    """Model for storing different types of activities"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    """Model for storing fitness activities"""
    UNIT_CHOICES = (
        ('km', 'Kilometers'),
        ('mi', 'Miles'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, related_name='activities')
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(blank=True, null=True)
    distance_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='km', blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type.name} on {self.date}"