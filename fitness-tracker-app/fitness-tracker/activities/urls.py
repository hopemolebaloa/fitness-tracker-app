# activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityTypeListView, activity_metrics

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    path('activities/types/', ActivityTypeListView.as_view(), name='activity-types'),
    path('activities/metrics/', activity_metrics, name='activity-metrics'),
]