from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.api.renderers import UserJSONRenderer
from apps.authentication.api.serializers import (RegistrationSerializer,
                                                 LoginSerializer, ResetPasswordRequestSerializer,
                                                 ResetPasswordSerializer)
from apps.authentication.models import User
from apps.core.database import get_query_set, get_model_object
from apps.core.utils import jwt_decode
from apps.core.views import get_request_data


class RegistrationViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        user = get_request_data(request)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication credentials not provided!")
        queryset = get_query_set(User)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = get_request_data(request)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        user = get_request_data(request)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Instructions on how to reset"
                                    "password have been sent to your email."},
                        status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def patch(self, request, token):
        payload = jwt_decode(token=token)
        user = get_model_object(model=User, column_name="user_uuid", column_value=payload.get("user_uuid"))
        password_data = get_request_data(request)
        serializer = self.serializer_class(data=password_data, instance=user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(dict(message="Password reset successfully"), status=status.HTTP_200_OK)
