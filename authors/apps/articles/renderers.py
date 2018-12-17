import json

from rest_framework.renderers import JSONRenderer


class ArticlesJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if len(data) == 1:
            return json.dumps({'article': data})
        return json.dumps({'articles': data})
