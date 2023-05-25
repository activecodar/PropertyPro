from rest_framework.exceptions import PermissionDenied


def get_request_data(request):
    return request.data or {}


def check_ownership(owner_field, request):
    if owner_field != request.user:
        raise PermissionDenied("You are not authorized to make changes to this record!")