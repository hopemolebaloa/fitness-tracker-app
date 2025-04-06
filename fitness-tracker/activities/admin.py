from django.contrib import admin
from .models import Activity, ActivityType

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    list_filter = ('activity_type', 'date', 'user')
    search_fields = ('user__username', 'user__email', 'activity_type__name', 'notes')
    date_hierarchy = 'date'
