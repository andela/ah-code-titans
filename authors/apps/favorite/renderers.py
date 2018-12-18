import json

from ..authentication.renderers import UserJSONRenderer


class FavoriteJSONRenderer(UserJSONRenderer):

    def render(self, data, media_type=None, renderer_context=None):
        """
        overide UserJSONRenderer to render our data under the "favorited" namespace.
        """
        return json.dumps({
            'favorited': data
        })
