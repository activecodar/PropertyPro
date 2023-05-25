import jwt
import os

from rest_framework.settings import api_settings


def jwt_decode(token=None):
    if token:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms="HS256"
        )
        return payload
    else:
        return None


def set_metadata(renderer_context, data):
    """
    Sets pagination data as metadata in the request
    :param renderer_context:
    :param data:
    """
    if renderer_context is not None and 'count' in data:
        response = renderer_context.get('response')
        page_size = api_settings.PAGE_SIZE
        response['Data-Count'] = data['count']
        response['Pages-Count'] = int(data['count'] / page_size) if int(data['count'] / page_size) > 0 or data[
            'count'] == 0 else 1
        response['Link-Previous-Page'] = data['previous']
        response['Link-Next-Page'] = data['next']