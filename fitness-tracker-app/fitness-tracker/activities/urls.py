# activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityTypeViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activity-types', ActivityTypeViewSet, basename='activity-type')

urlpatterns = [
    path('', include(router.urls)),
]