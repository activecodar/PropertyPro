from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.database import get_query_set, get_model_object
from apps.core.views import get_request_data, check_ownership
from apps.property.api.renderers import PropertyJSONRenderer
from apps.property.api.serializers import PropertySerializer
from apps.property.api.service import property_service
from apps.property.models import Property


class PropertyViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (PropertyJSONRenderer,)
    serializer_class = PropertySerializer

    def create(self, request):
        property_details = get_request_data(request)
        serializer = self.serializer_class(data=property_details)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['owner'] = request.user
        property_service.create(validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = get_query_set(Property)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
