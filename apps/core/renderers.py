import json

from rest_framework.renderers import JSONRenderer

from apps.core.utils import set_metadata


class DefaultJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self, data, media_type=None, renderer_context=None):
        if data.get('results', None) is not None:
            set_metadata(renderer_context=renderer_context, data=data)
            return json.dumps(data['results'])

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        elif data.get('errors', None) is not None:
            return super(DefaultJSONRenderer, self).render(data)

        else:
            return json.dumps(data)