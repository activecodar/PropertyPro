from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.property.api.views import PropertyViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'properties', PropertyViewSet, basename='properties')

urlpatterns = [
    path('', include(router.urls)),
]