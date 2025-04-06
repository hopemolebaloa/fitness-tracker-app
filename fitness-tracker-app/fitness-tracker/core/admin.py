from django.contrib import admin
from .models import Goal

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'activity_type', 'target_value', 'metric', 'period', 'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed', 'period', 'metric', 'activity_type')
    search_fields = ('user__username', 'user__email', 'title', 'activity_type__name')
    date_hierarchy = 'created_at'
