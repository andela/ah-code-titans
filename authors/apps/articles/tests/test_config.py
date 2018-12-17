class TestConfig():
    """ Configurations for all tests"""

    article_data = {
        "article": {
            "title": "javascript es6",
            "tag_list": ["kimame", "kenya"],
            "description": "introduction to es6",
            "body": "intermediate js developers"
        }
    }
    article_data_invalid_tag_field = {
        "article": {
            "title": "javascript es6",
            "tag_list": "kimame",
            "description": "introduction to es6",
            "body": "intermediate js developers"
        }
    }
    update_article_data = {
        "article": {
            "title": "javascript es6",
            "tag_list": ["Shomie", "Homie"],
            "description": "introduction to es6",
            "body": "intermediate js developers"
        }
    }
    article_data_2 = {
        "article": {
            "title": "javascript es7",
            "tag_lst": [],
            "description": "introduction to es7",
            "body": "intermediate js developers"
        }
    }
    article_data_no_taglist = {
        "article": {
            "title": "javascript es7",
            "description": "introduction to es7",
            "body": "intermediate js developers"
        }
    }
    article_data_invalid_tag = {
        "article": {
            "title": "javascript es7",
            "tag_list": [1, "Homie"],
            "description": "introduction to es7",
            "body": "intermediate js developers"
        }
    }
