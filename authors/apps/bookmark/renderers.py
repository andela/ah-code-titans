import json

from rest_framework.renderers import JSONRenderer


class BookmarksJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # breakpoint()

        if len(data) < 1:
            return json.dumps({'message': "You have not bookmarked any article"})
        return json.dumps({'bookmarks': data})
