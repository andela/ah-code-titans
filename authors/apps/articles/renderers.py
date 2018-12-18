import json

from rest_framework.renderers import JSONRenderer


class ArticlesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        return json.dumps({'articles': data})
